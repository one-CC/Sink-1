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


class ControlShow:
    @staticmethod
    def show_msg():
        '''
        下行控制
        '''
        '''
        小车方向电机控制
        '''
        print('小车方向电机控制')
        print('前：$1,0,0,0,0,0,0,0,0#')
        print('后：$2,0,0,0,0,0,0,0,0#')
        print('左：$3,0,0,0,0,0,0,0,0#')
        print('右：$4,0,0,0,0,0,0,0,0#')
        print('左转：$0,1,0,0,0,0,0,0,0#')
        print('右转：$0,2,0,0,0,0,0,0,0#')
        print('停：$0,0,0,0,0,0,0,0,0#')
        '''
        摄像头电机方向控制
        '''
        print('摄像头电机方向控制')
        print('前：$0,0,0,0,3,0,0,0,0#')
        print('后：$0,0,0,0,4,0,0,0,0#')
        print('左：$0,0,0,0,6,0,0,0,0#')
        print('右：$0,0,0,0,7,0,0,0,0#')
        print('停：$0,0,0,0,8,0,0,0,0#')
        '''
        超声波电机控制
        '''
        print('超声波电机控制')
        print('左：$0,0,0,0,1,0,0,0,0#')
        print('中：$0,0,0,0,0,0,0,0,1#')
        print('右：$0,0,0,0,2,0,0,0,0#')
        '''
        灯控制
        '''
        print('灯控制')
        print('开：$0,0,0,0,0,0,1,0,0#')
        print('关：$0,0,0,0,0,0,8,0,0#')
        print('红：$0,0,0,0,0,0,2,0,0#')
        print('绿：$0,0,0,0,0,0,3,0,0#')
        print('蓝：$0,0,0,0,0,0,4,0,0#')

        '''
        其他功能
        '''
        print('其他功能')
        print('灭火：$0,0,0,0,0,0,0,1,0#')
        print('鸣笛：$0,0,1,0,0,0,0,0,0#')
        print('加速：$0,0,0,1,0,0,0,0,0#')
        print('减速：$0,0,0,2,0,0,0,0,0#')

        '''
        转动角度控制
        '''
        # print("舵机转动到180度：$4WD,PTZ180#")

        '''
        上行显示
        '''
        '''
        小车超声波传感器采集的信息发给上位机显示
        打包格式如:
            超声波 电压  灰度  巡线  红外避障 寻光
        $4WD,CSB120,PV8.3,GS214,LF1011,HW11,GM11#
        '''

    @staticmethod
    def show_key():
        print('小车方向控制')
        print('前：w，后：x，左：a，右：d，左转：z，右转：c，停：s')
        print('摄像头方向控制')
        print('上：i，下：m，左：j，右：l，停：k')
        print('超声波方向控制')
        print('左：r，中：t，右：y')
        print('灯开关控制')
        print('开：v，关：b')
        print('其他功能')
        print('鸣笛：f，灭火：g')


class ControlKeyboard:
    def __init__(self, keyboard_input):
        self.KEYBOARD_INPUT = keyboard_input

    def get_control(self):
        """

        :return:
        """
        msg = []
        # 小车方向
        if self.KEYBOARD_INPUT == 'w':  # 前
            msg.append('$1,0,0,0,0,0,0,0,0#')
            msg.append('$0,0,0,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'x':  # 后
            msg.append('$2,0,0,0,0,0,0,0,0#')
            msg.append('$0,0,0,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'a':  # 左
            msg.append('$3,0,0,0,0,0,0,0,0#')
            msg.append('$0,0,0,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'd':  # 右
            msg.append('$4,0,0,0,0,0,0,0,0#')
            msg.append('$0,0,0,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'z':  # 左转
            msg.append('$0,1,0,0,0,0,0,0,0#')
            msg.append('$0,0,0,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'c':  # 右转
            msg.append('$0,2,0,0,0,0,0,0,0#')
            msg.append('$0,0,0,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 's':  # 停
            msg.append('$0,0,0,0,0,0,0,0,0#')

        # 摄像头方向
        elif self.KEYBOARD_INPUT == 'i':  # 上
            msg.append('$0,0,0,0,3,0,0,0,0#')
            # msg.append('$0,0,0,0,8,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'm':  # 下
            msg.append('$0,0,0,0,4,0,0,0,0#')
            # msg.append('$0,0,0,0,8,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'j':  # 左
            msg.append('$0,0,0,0,6,0,0,0,0#')
            # msg.append('$0,0,0,0,8,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'l':  # 右
            msg.append('$0,0,0,0,7,0,0,0,0#')
            # msg.append('$0,0,0,0,8,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'k':  # 停
            msg.append('$0,0,0,0,8,0,0,0,0#')

        # 超声波控制
        elif self.KEYBOARD_INPUT == 'r':  # 左
            msg.append('$0,0,0,0,1,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 't':  # 中
            msg.append('$0,0,0,0,0,0,0,0,1#')
        elif self.KEYBOARD_INPUT == 'y':  # 右
            msg.append('$0,0,0,0,2,0,0,0,0#')

        # 灯开关控制
        elif self.KEYBOARD_INPUT == 'v':  # 开
            msg.append('$0,0,0,0,0,0,1,0,0#')
        elif self.KEYBOARD_INPUT == 'b':  # 关
            msg.append('$0,0,0,0,0,0,8,0,0#')

        # 其他功能
        elif self.KEYBOARD_INPUT == 'f':  # 鸣笛
            msg.append('$0,0,1,0,0,0,0,0,0#')
        elif self.KEYBOARD_INPUT == 'g':  # 灭火
            msg.append('$0,0,0,0,0,0,0,1,0#')

        return msg


class Car:
    def __init__(self, car_number):
        self.car_number = car_number
        self.position = None
        self.accelerate = None
        self.angle = None
        self.connected = False
        self.socket = None

    # 把每个小车作为一个线程单独接收。
    def receive(self):
        file = open('./car_logs/car_{0}.txt'.format(self.car_number), mode='a')
        try:
            while True:
                data = self.socket.recv(1024)
                if not data:
                    break
                print("收到来自小车 {0} 的消息：{1}".format(self.car_number, data.decode('utf-8')))
                # Car的每个包只包含一个ACC、Angle、GPS，包之间用一个#分隔，包内变量间用；分隔，变量的分量之间用，分隔。
                messages = (data.decode('utf-8')).split('#')
                variables = messages[-2].split(';')  # 最后一个是空字符串
                v1 = variables[0].split(',')
                v2 = variables[1].split(',')
                v3 = variables[2].split(',')
                lock.acquire()
                self.accelerate = [float(v1[0]), float(v1[1]), float(v1[2])]
                self.angle = [float(v2[0]), float(v2[1]), float(v2[2])]
                self.position = [float(v3[0]), float(v3[1])]
                lock.release()

                format_str = "加速度：{0}\t\t角度：{1}\t\tGPS：{2}".format(self.accelerate, self.angle, self.position)
                time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                file.write("{0} 来自小车 {1} ：{2}\n".format(time_string, self.car_number, format_str))
        except ConnectionResetError:
            print("小车 {0} 主动断开tcp连接！".format(self.car_number))
        except:
            traceback.print_exc()
            print("小车 {0} 的tcp连接出问题了！".format(self.car_number))
        finally:
            file.close()
            self.connected = False
            print("小车 {0} 的tcp连接已断开！".format(self.car_number))

    def send(self, message):
        self.socket.send(message.encode('utf-8'))


class UWB:
    def __init__(self, uwb_number, position):
        self.distance = 0
        self.uwb_number = uwb_number
        self.position = position
        self.connected = False
        self.socket = None

    def receive(self):
        file = open('./uwb_logs/uwb_{0}.txt'.format(self.uwb_number), mode='a')
        try:
            while True:
                data = self.socket.recv(1024)
                if not data:
                    break
                print("收到来自UWB {0} 的消息：{1}".format(self.uwb_number, data.decode('utf-8')))
                time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                file.write("{0} 来自UWB {1} ：{2}\n".format(time_string, self.uwb_number, data.decode('utf-8')))
                # UBW的每个包只包含一个distance，包之间用一个#分隔
                messages = (data.decode('utf-8')).split('#')
                lock.acquire()
                self.distance = float(messages[-2])  # 最后一个是空字符串
                lock.release()
        except ConnectionResetError:
            print("UWB {0} 主动断开tcp连接！".format(self.uwb_number))
        except:
            traceback.print_exc()
            print("UWB {0} 的tcp连接出问题了！".format(self.uwb_number))
        finally:
            file.close()
            self.connected = False
            print("UWB {0} 的tcp连接已断开！".format(self.uwb_number))

    def send(self, cmd):
        # cmd = 'start','stop',...
        self.socket.send(cmd.encode('utf-8'))


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
# host = '192.168.43.230'
port = 8888
host = '127.0.0.1'
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
    main(test=False)
