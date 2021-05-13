# -*- coding utf-8 -*-
# @Time : 2021/1/4 19:57
# @Author : DH
# @File : models.py
# @Software : PyCharm
import threading
import traceback
import time
from datetime import datetime
from gps_transform import gps_transform


class ControlShow:
    @staticmethod
    def show_msg():
        """
        下行控制
        """
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
        self.gps = None
        self.accelerate = None
        self.angle = None
        self.connected = False
        self.socket = None
        self.position = [0, 0]

    # 把每个小车作为一个线程单独接收。
    def receive(self):
        file = open('./car_logs/car_{0}_{1}.txt'.format(self.car_number, datetime.now().strftime('%m_%d')), mode='a')
        file.write("************* 开始测试，时间：" +
                   datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + " *************" + '\n')
        try:
            while True:
                # 倒数最后一个数据包可能会被截断，将导致解析错误；
                # TCP 接收buffer大小；
                # 刚开始 连接-断开-连接
                data = self.socket.recv(10240)
                if len(data) == 0:
                    break
                # print("收到来自小车 {0} 的消息：{1}".format(self.car_number, data.decode('utf-8')))
                # if len(data) >= 74:
                if len(data) >= 40:
                    # Car的每个包只包含一个ACC、Angle、GPS，包之间用一个#分隔，包内变量间用；分隔，变量的分量之间用，分隔。
                    try:
                        messages = (data.decode('utf-8')).split('#')
                        variables = messages[-2].split(';')  # 最后一个是空字符串
                        v1 = variables[0].split(',')
                        v2 = variables[1].split(',')
                        v3 = variables[2].split(',')
                        self.accelerate = [float(v1[0]), float(v1[1]), float(v1[2])]
                        # 正常情况下，xyz 东北天
                        self.angle = [float(v2[0]), float(v2[1]), float(v2[2])]
                        self.gps = [float(v3[0]), float(v3[1])]
                        self.position = gps_transform(self.gps)
                    except Exception:
                        traceback.print_exc()
                    format_str = "加速度：{0}    角度：{1}    GPS：{2}".format(self.accelerate, self.angle, self.gps)
                    time_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    file.write("{0} ：{1}\n".format(time_string, format_str))
        except ConnectionResetError:
            print("小车 {0} 主动断开tcp连接！".format(self.car_number))
        except:
            traceback.print_exc()
            print("小车 {0} 的tcp连接出问题了！".format(self.car_number))
        finally:
            file.write("************* 结束测试，时间：" +
                       datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + " *************\n\n")
            file.close()
            self.connected = False
            print("小车 {0} 的tcp连接已断开！".format(self.car_number))

    def send(self, message):
        self.socket.send(message.encode('utf-8'))

    def __str__(self):
        return "Car:{0}".format(self.car_number)


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
                self.distance = float(messages[-2])  # 最后一个是空字符串
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

    def get_distance(self):
        res, self.distance = self.distance, 0
        return res

