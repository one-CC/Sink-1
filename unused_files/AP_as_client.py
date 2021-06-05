# -*- coding: utf-8 -*-
# @Time : 2020/7/15 20:19
# @Author : DH
# @Site : 
# @File : AP_as_client.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time : 2020/7/8 21:09
# @Author : DH
# @Site :
# @File : car_control.py
# @Software: PyCharm
import concurrent.futures as futures
import time
import msvcrt
import socket
import threading
import queue
lock = threading.Lock()


class Car:
    def __init__(self, ip, port, number):
        self.num = number
        self.ip = ip
        self.port = port
        self.addr = (self.ip, self.port)
        self.connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_socket(self):
        try:
            self.socket.connect(self.addr)
        except:
            print("连接失败")
        else:
            self.connected = True

    def close_socket(self):
        if self.connected:
            self.socket.close()
            self.connected = False

    def receive(self):
        if self.connected:
            try:
                while True:
                    data = self.socket.recv(1024)
                    if not data:
                        break
                    print("接收小车 {0} 发来的消息：{1}".format(self.num, data.decode('utf-8')))
            except:
                print("连接中断")
            finally:
                print("小车 {} 的TCP连接已断开！".format(self.num))
                self.close_socket()

    def send(self, msg):
        if self.connected:
            self.socket.send(msg.encode('utf-8'))


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

        return msg[0]


host = '192.168.31.99'
port = 8888
car_list = []
car_list.append(Car(host, port, 1))
thread_list = []


def main():
    while True:
        try:
            keyboard_input = msvcrt.getch().decode('utf-8')
            if keyboard_input == "\x1b":
                print("客户端关闭！")
                break
            data = ControlKeyboard(keyboard_input).get_control()
            number = input("发送给第几个小车？目前小车列表为:\r\n{0}\r\n".format([car.num for car in car_list]))
            print("Send data to car {0}：{1}".format(number, str(data)))
            car_list[int(number)-1].send(data)
            time.sleep(0.2)
        finally:
            pass


if __name__ == '__main__':
    ControlShow.show_key()
    for car in car_list:
        car.connect_socket()
        if car.connected:
            thread = threading.Thread(target=car.receive)
            thread.setDaemon(True)
            thread.start()
            thread_list.append(thread)
    main()
