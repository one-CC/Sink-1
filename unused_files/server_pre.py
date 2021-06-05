# -*- coding utf-8 -*-
# @Time : 2021/1/12 13:47
# @Author : DH
# @File : server_pre.py
# @Software : PyCharm
import time
import msvcrt
import math
import traceback
import numpy as np
import socket
import threading
import matplotlib.pyplot as plt
from location import trilateration
from car_control import top3_closest_cars, move_forward_target
from gps_transform import gps_transform
from models import Car, UWB


total_car_number = 5
ip2CarNumber = {
    '192.168.31.99': 1,
    # '169.254.62.154': 2,
    '192.168.2.16': 3,
    '192.168.43.51': 4,
}
ip2UWB = {
    '192.168.43.253': 1,
    '192.168.43.141': 2,
    '127.0.0.1': 3,
}
car_map = {}
for i in range(1, total_car_number + 1):
    car_map[i] = Car(i)
uwb_map = {}
uwb_gps = [[103.92792, 30.75436], [103.92768, 30.75445], [0, 0]]
for i in range(1, 4):
    uwb_map[i] = UWB(i, gps_transform(uwb_gps[i - 1]))

lock = threading.Lock()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = '192.168.43.230'
port = 8888
host = '127.0.0.1'
# port = 6666
server.bind((host, port))
server.listen(total_car_number + 3)


def bind_socket():
    """
    监听小车的连接请求
    :return:
    """
    print("等待连接中...")
    while True:
        try:
            client, addr = server.accept()
            if client:
                global car_map, uwb_map
                if ip2UWB.get(addr[0], None):
                    # 如果是UWBip地址，则需要建立单独的线程来控制uwb；
                    uwb_number = ip2UWB[addr[0]]
                    uwb = uwb_map[uwb_number]
                    # 如果对应uwb没有活跃的连接线程，则创建线程；否则，忽视。
                    if not uwb.connected:
                        uwb.socket = client
                        uwb.connected = True
                        thread = threading.Thread(target=uwb.receive)
                        thread.setDaemon(True)
                        thread.start()
                    print("UWB {0} 已连接！".format(uwb_number))
                elif ip2CarNumber.get(addr[0], None):
                    # 如果为小车地址；
                    car_number = ip2CarNumber[addr[0]]
                    car = car_map[car_number]
                    # 如果对应小车没有活跃的连接线程，则创建线程；否则，忽视。
                    if not car.connected:
                        car.socket = client
                        car.connected = True
                        thread = threading.Thread(target=car.receive)
                        thread.start()
                    print("小车 {0} 已连接！".format(car_number))
                    # send_msg = "你已经接入系统，" + str(addr[0]) + '！'
                    # buffersize = car.send(send_msg)
                    # print("发送了{0}个比特过去".format(buffersize))
                else:
                    pass
        except:
            print("服务器取消监听了！！！")
            break


def main(test):
    # p0 = gps_transform([103.92388, 30.74216])
    # p1 = gps_transform([103.93755, 30.75348])
    # 下面这组GPS区域用于楼顶测试
    p0 = gps_transform([103.92943, 30.75131])
    p1 = gps_transform([103.93025, 30.75208])
    area_x = [p0[0], p1[0]]
    area_y = [p0[1], p1[1]]
    file = open('2uwb_test.txt', mode='a')
    fig = plt.figure()
    try:
        while True:
            d1 = uwb_map[1].get_distance()
            d2 = uwb_map[2].get_distance()
            d3 = uwb_map[3].get_distance()
            if d1 != 0 and d2 != 0 and d3 != 0:
                target_position = trilateration(uwb_map[1].position, uwb_map[2].position, uwb_map[3].position,
                                                d1, d2, d3)
                selected_cars = top3_closest_cars(target_position, car_map)
                for car in selected_cars:
                    move_forward_target(car, target_position)
            if test:
                keyboard_input = msvcrt.getch().decode('utf-8')
                if keyboard_input == '\x1b':
                    print("服务器关闭！")
                    break
            # data = ControlKeyboard(keyboard_input).get_control()
            # active_cars = [1 if car.connected else 0 for car in car_map.values()]
            # number = input("发送给第几个小车？目前连接的小车有:\r\n{0}\r\n".format(active_cars))
            # print("发送给小车 {0}:{1}".format(number, str(data)))
            # for d in data:
            #     car_map[int(number)].send(d)
            #     time.sleep(0.2)
    except Exception:
        traceback.print_exc()
    finally:
        print("服务器关闭！")
        file.close()


if __name__ == '__main__':
    listen_thread = threading.Thread(target=bind_socket)
    listen_thread.setDaemon(True)
    listen_thread.start()
    main(test=False)

