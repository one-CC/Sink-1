# -*- coding utf-8 -*-
# @Time : 2021/9/1 19:51
# @Author : donghao
# @File : aio_server_uwb.py
# @Desc : 整个异步sink节点的预实现
import asyncio
import json
import socket
import traceback
import time

import aiofiles
import aiohttp
from aiofiles.threadpool import AsyncTextIOWrapper

from car_control import *
from gps_transform import position_transform
from location import trilateration
from models import Car, UWB
from utils import *

ROOT_PATH = get_root_path()
total_car_number = 6
ip2CarNumber = {
    '192.168.43.173': 1,
    '192.168.43.192': 2,
    '192.168.43.133': 3,
    '192.168.43.185': 4,
    '192.168.43.100': 5,
    '192.168.43.190': 6,
}
ip2UWBNumber = {
    '192.168.43.253': 1,
    '192.168.43.141': 2,
    '192.168.43.142': 3,
}
car_map = {}
for i in range(1, total_car_number + 1):
    car_map[i] = Car(i)
uwb_map = {}
# 每次测试需要手动填入三个 uwb 的 gps 信息
uwb_gps = [[103.92792, 30.75436], [103.92768, 30.75445], [0, 0]]
for i in range(1, 4):
    uwb_map[i] = UWB(i, uwb_gps[i - 1])
# 协程map, key为小车编号
coroutine_map = {}


def accept_socket(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    ip = writer.get_extra_info("peername")[0]
    global car_map, uwb_map
    if ip2UWBNumber.get(ip, None):
        # 如果是UWBip地址，则需要建立单独的线程来控制uwb；
        uwb_number = ip2UWBNumber[ip]
        uwb = uwb_map[uwb_number]
        # 如果对应uwb没有活跃的连接线程，则创建线程；否则，忽视。
        if not uwb.connected:
            uwb.connect_uwb(reader)
            asyncio.create_task(uwb.receive())
            print("UWB {0} 已连接！".format(uwb.uwb_number))
    elif ip2CarNumber.get(ip, None):
        # 如果为小车地址；
        car_number = ip2CarNumber[ip]
        car = car_map[car_number + i]
        # 如果对应小车没有建立连接，则连接并创建receive协程
        if not car.connected:
            car.connect_car(reader, writer)
            t = asyncio.create_task(car.receive())
            coroutine_map[car.car_number] = t
            print("小车 {0} 已连接！".format(car.car_number))


async def listen_socket():
    """ 监听小车和uwb的连接请求 """
    server = await asyncio.start_server(accept_socket, host="192.168.43.231", port=8888, family=socket.AF_INET)
    print("等待连接中...")
    try:
        await server.serve_forever()
    except asyncio.CancelledError:
        print('listen_socket() was cancelled')
    finally:
        server.close()
        await server.wait_closed()


async def post_data(session: aiohttp.ClientSession):
    """ 上传各个小车的数据给后台服务器 """
    url = "http://192.168.43.29:8080/car/insert"
    headers = {'content-type': 'application/json'}
    try:
        while True:
            data_list = []
            for car in car_map.values():
                base_map = dict()
                base_map["number"] = car.car_number
                base_map["gps"] = car.gps
                base_map["angle"] = car.angle
                base_map["battery"] = car.battery
                base_map["connected"] = car.connected
                data_list.append(base_map)
            json_data = json.dumps(data_list)
            if session.closed:
                break
            await session.post(url=url, data=json_data, headers=headers)
            await asyncio.sleep(1.0)
    except asyncio.CancelledError:
        print('post_data(session) was cancelled')


def heart_beat_check():
    """ Sink端应用层心跳机制 """
    for car in car_map.values():
        if car.connected and int(time.time()) - car.last_upstream_time > 5:
            car.close_car()
            coroutine_map[car.car_number].cancel()
            coroutine_map[car.car_number] = None


async def main():
    asyncio.create_task(listen_socket())

    cmd_log = await aiofiles.open('{0}/logs/car_logs/car_cmd_{1}.txt'.format(
        ROOT_PATH, datetime.now().strftime('%m_%d')), mode='a')  # type: AsyncTextIOWrapper
    await cmd_log.write("************* 开始测试，时间：" + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                        + " *************" + '\n')
    target_log = await aiofiles.open('{0}/logs/uwb_logs/target_gps_{1}.txt'.format(
        ROOT_PATH, datetime.now().strftime('%m_%d')), mode='a')
    await target_log.write("************* 开始测试，时间：" + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                           + " *************" + '\n')
    cars = [car_map[5]]
    while not all_cars_connected(car_list=car_map):
        await asyncio.sleep(0.1)
    while not all_uwbs_connected(uwb_map):
        await asyncio.sleep(0.1)

    # session = aiohttp.ClientSession()
    # asyncio.create_task(post_data(session))
    try:
        while True:
            await asyncio.sleep(1)
            # 心跳检测
            if int(time.time()) % 10 == 0:
                heart_beat_check()
            d1 = uwb_map[1].get_distance()
            d2 = uwb_map[2].get_distance()
            d3 = uwb_map[3].get_distance()
            if d1 == 0 or d2 == 0 or d3 == 0:
                await asyncio.sleep(0.1)
                continue
            target_position = trilateration(uwb_map[1].position, uwb_map[2].position, uwb_map[3].position, d1, d2, d3)
            target_gps = position_transform(target_position)
            # selected_cars = top3_closest_cars(target_position, car_map)
            # if len(selected_cars) < 3:
            #     print("可用小车数小于3！")
            #     break
            selected_cars = cars
            for car in selected_cars:
                if not car.connected:
                    # 可能选出三辆小车后，断连，此时不应发送消息
                    continue
                info = await move_forward_target(car, target_position, variable_speed=True)
                await cmd_log.write(info + '\n')
            await target_log.write("{0}：{1}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], target_gps))
    except Exception:
        traceback.print_exc()
    finally:
        print("服务器关闭！")
        await cmd_log.write("************* 结束测试，时间：" + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                            + " *************" + '\n\n')
        await cmd_log.close()
        await target_log.write("************* 结束测试，时间：" + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                               + " *************" + '\n\n')
        await target_log.close()
        # await session.close()
        await asyncio.sleep(1.0)


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("键盘中断！")
        for task in asyncio.Task.all_tasks():
            task.cancel()  # 取消所有的Task
        while not all_tasks_done():
            event_loop.stop()  # 停止本次事件循环
            event_loop.run_forever()  # 开启下轮事件循环，在下轮事件循环中被取消的Task对象将抛出asyncio.CancelledError
    event_loop.close()
