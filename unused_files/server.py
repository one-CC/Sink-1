# -*- coding: utf-8 -*-
# @Time : 2020/7/8 21:09
# @Author : DH
# @Site :
# @File : car_control.py
# @Software: PyCharm
import time
import msvcrt
import math
import traceback
import numpy as np
import socket
import threading
import matplotlib.pyplot as plt
from location import trilateration
from gps_transform import gps_transform
from models import Car, ControlShow, ControlKeyboard, UWB


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
    uwb_map[i] = UWB(i, uwb_gps[i - 1])

lock = threading.Lock()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.43.230'
port = 8888
# host = '127.0.0.1'
# port = 6666
server.bind((host, port))
server.listen(total_car_number + 3)


# 监听小车的连接请求
def bind_socket():
    print("等待连接中...")
    while True:
        try:
            client, addr = server.accept()
            if client:
                lock.acquire()
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
                lock.release()
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
    while True:
        try:
            # 两个uwb时的测试图形
            if uwb_map[1].distance != 0 and uwb_map[2].distance != 0:
                theta = np.arange(0, 2 * math.pi, 0.01)
                center1 = gps_transform(uwb_map[1].position)
                x1 = uwb_map[1].distance * np.cos(theta) + center1[0]
                y1 = uwb_map[1].distance * np.sin(theta) + center1[1]
                center2 = gps_transform(uwb_map[2].position)
                x2 = uwb_map[2].distance * np.cos(theta) + center2[0]
                y2 = uwb_map[2].distance * np.sin(theta) + center2[1]
                plt.plot(x1, y1, '-r', x2, y2, '--b')
                # plt.xlim(0, 100)
                # plt.ylim(0, 100)
                plt.pause(0.2)
                plt.cla()
                s = "UWB1的距离：{0}\t\tUWB2的距离：{1}\n".format(uwb_map[1].distance, uwb_map[2].distance)
                file.write(s)
                lock.acquire()
                uwb_map[1].distance, uwb_map[2].distance = 0, 0
                lock.release()

            # lock.acquire()
            # if uwb_map[0].distance != 0 and uwb_map[1].distance != 0 and uwb_map[2].distance != 0:
            #     target_position = trilateration(uwb_map[0].position, uwb_map[1].position, uwb_map[2].position,
            #                                     uwb_map[0].distance, uwb_map[1].distance, uwb_map[2].distance)
            # lock.release()
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
            file.close()
            traceback.print_exc()
    file.close()


if __name__ == '__main__':
    ControlShow.show_key()
    listen_thread = threading.Thread(target=bind_socket)
    listen_thread.setDaemon(True)
    listen_thread.start()
    main(test=True)
