# -*- coding utf-8 -*-
# @Time : 2021/5/29 17:15
# @Author : DH
# @Software : PyCharm
# @Desc : 一辆车追踪另一辆车的异步版本
import json
import socket
import traceback
import time
import asyncio

import aiofiles
import aiohttp
from aiofiles.threadpool import AsyncTextIOWrapper

from car_control import *
from models import Car, UWB
from utils import *

ROOT_PATH = get_root_path()
total_car_number = 6
ip2CarNumber = {
    '192.168.43.82': 1,
    '192.168.43.64': 2,
    '192.168.43.40': 3,
    '192.168.43.47': 4,
    '192.168.43.21': 5,
    '192.168.43.242': 6,
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
        car = car_map[car_number]
        # 如果对应小车没有建立连接，则连接并创建receive协程
        if not car.connected:
            car.connect_car(reader, writer)
            t = asyncio.create_task(car.receive())
            coroutine_map[car.car_number] = t
            print("小车 {0} 已连接！".format(car.car_number))


async def listen_socket():
    """ 监听小车和uwb的连接请求 192.168.43.230"""
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
    url = "http://192.168.43.35:8080/car/insert"
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

    target_car = car_map[1]
    cars = [car_map[1], car_map[2], car_map[3], car_map[4], car_map[5]]

    while not target_car.connected or not all_cars_connected(car_list=cars):
        await asyncio.sleep(0.1)

    session = aiohttp.ClientSession()
    asyncio.create_task(post_data(session))

    try:
        while True:
            # if int(time.time()) % 10 == 0:
            #     heart_beat_check()
            selected_cars = top3_best_cars(target_car.position, cars)
            if len(selected_cars) < 3:
                print("可调度节点小于3！")
                break
            for car in selected_cars:
                if not car.connected:
                    # 可能选出三辆小车后，断连，此时不应发送消息
                    continue
                info = await move_forward_target(car, target_car.position, variable_speed=True)
                await cmd_log.write(info + '\n')
    except asyncio.CancelledError:
        print('main() was cancelled')
    except Exception:
        traceback.print_exc()
    finally:
        await cmd_log.write("************* 结束测试，时间：" + datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                            + " *************" + '\n\n')
        await cmd_log.close()
        await session.close()
        await asyncio.sleep(1)
        print("服务器关闭！")


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("键盘中断！")
        for task in asyncio.Task.all_tasks():
            task.cancel()   # 取消所有的Task
        while not all_tasks_done():
            event_loop.stop()   # 停止本次事件循环
            event_loop.run_forever()    # 开启下轮事件循环，在下轮事件循环中被取消的Task对象将抛出asyncio.CancelledError
    event_loop.close()
