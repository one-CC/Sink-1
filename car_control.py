# -*- coding utf-8 -*-
# @Time : 2021/1/12 14:47
# @Author : DH
# @File : car_control.py
# @Software : PyCharm
import math
import time
from datetime import datetime


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


def get_control(cmd):
    """
    根据cmd，返回相应的指令
    :param cmd:     要完成的动作
    :return:    控制小车的指令
    """
    msg = []
    # 小车方向
    if cmd == 'w':  # 前
        msg.append('$1,0,0,0,0,0,0,0,0#')
        msg.append('$0,0,0,0,0,0,0,0,0#')
    elif cmd == 'x':  # 后
        msg.append('$2,0,0,0,0,0,0,0,0#')
        msg.append('$0,0,0,0,0,0,0,0,0#')
    elif cmd == 'a':  # 左
        msg.append('$3,0,0,0,0,0,0,0,0#')
        msg.append('$0,0,0,0,0,0,0,0,0#')
    elif cmd == 'd':  # 右
        msg.append('$4,0,0,0,0,0,0,0,0#')
        msg.append('$0,0,0,0,0,0,0,0,0#')
    elif cmd == 'z':  # 左转
        msg.append('$0,1,0,0,0,0,0,0,0#')
        msg.append('$0,0,0,0,0,0,0,0,0#')
    elif cmd == 'c':  # 右转
        msg.append('$0,2,0,0,0,0,0,0,0#')
        msg.append('$0,0,0,0,0,0,0,0,0#')
    elif cmd == 's':  # 停
        msg.append('$0,0,0,0,0,0,0,0,0#')

    # 灯开关控制
    elif cmd == 'v':  # 开
        msg.append('$0,0,0,0,0,0,1,0,0#')
    elif cmd == 'b':  # 关
        msg.append('$0,0,0,0,0,0,8,0,0#')

        # 摄像头方向
    elif cmd == 'i':  # 上
        msg.append('$0,0,0,0,3,0,0,0,0#')
        # msg.append('$0,0,0,0,8,0,0,0,0#')
    elif cmd == 'm':  # 下
        msg.append('$0,0,0,0,4,0,0,0,0#')
        # msg.append('$0,0,0,0,8,0,0,0,0#')
    elif cmd == 'j':  # 左
        msg.append('$0,0,0,0,6,0,0,0,0#')
        # msg.append('$0,0,0,0,8,0,0,0,0#')
    elif cmd == 'l':  # 右
        msg.append('$0,0,0,0,7,0,0,0,0#')
        # msg.append('$0,0,0,0,8,0,0,0,0#')
    elif cmd == 'k':  # 停
        msg.append('$0,0,0,0,8,0,0,0,0#')

    # 超声波控制
    elif cmd == 'r':  # 左
        msg.append('$0,0,0,0,1,0,0,0,0#')
    elif cmd == 't':  # 中
        msg.append('$0,0,0,0,0,0,0,0,1#')
    elif cmd == 'y':  # 右
        msg.append('$0,0,0,0,2,0,0,0,0#')

    # 其他功能
    elif cmd == 'f':  # 鸣笛
        msg.append('$0,0,1,0,0,0,0,0,0#')
    elif cmd == 'g':  # 灭火
        msg.append('$0,0,0,0,0,0,0,1,0#')

    return msg


def calculate_angle(vector):
    """
    计算一个向量与平面x轴的夹角
    :param vector: 向量
    :return: 与x轴的夹角，范围[0, 360]
    """
    dist = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    angle = math.degrees(math.acos(vector[0] / dist))
    angle = angle if vector[1] > 0 else 360 - angle
    return round(angle, 2)


def move_forward_target(car, target_position):
    """
    根据小车与目标的位置，进行移动
    :param car:
    :param target_position:
    :return:
    """
    vector = [target_position[0] - car.position[0], target_position[1] - car.position[1]]
    distance = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    if distance <= 2:
        # 距离小于两米，则不移动
        msgs = get_control("s")
        info = "Action：原地不动"
        print("原地不动")
        for msg in msgs:
            car.send(msg)
            time.sleep(0.2)
        time_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        return "{0}：{1}".format(time_string, info)
    angle = calculate_angle(vector)

    # 将小车的三维角度投影到平面坐标中
    projected_car_angle = car.angle[2] if car.angle[2] >= 0 else 360 + car.angle[2]

    # 根据小车的朝向与目标向量的夹角，分情况：
    angle_diff = projected_car_angle - angle
    print("当前角度：", angle_diff)
    if math.fabs(angle_diff) <= 30 or math.fabs(angle_diff) >= 330:
        # 小夹角情况下，直接 向前走
        print("直接向前走")
        info = "Action：直接向前走"
        msgs = get_control("w")
    elif 30 < angle_diff <= 90 or -330 <= angle_diff < -270:
        # 右转
        print("右转")
        info = "Action：右转"
        msgs = get_control("d")
    elif -90 <= angle_diff < -30 or 270 <= angle_diff < 330:
        # 左转
        print("左转")
        info = "Action：左转"
        msgs = get_control("a")
    elif 90 < angle_diff <= 180 or -270 <= angle_diff < -180:
        # 原地右转
        print("原地右转")
        info = "Action：原地右转"
        msgs = get_control("c")
    elif -180 <= angle_diff < -90 or 180 < angle_diff < 270:
        # 原地左转
        print("原地左转")
        info = "Action：原地左转"
        msgs = get_control("z")
    for msg in msgs:
        car.send(msg)
        time.sleep(0.2)
    time_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return "{0}：位置向量的角度：{1}\t小车朝向角度：{2}\t{3}".format(time_string, angle, projected_car_angle, info)


def top3_closest_cars(target_position, car_map):
    """
    计算当前时刻距离目标最近的三个小车
    :param car_map:     小车字典
    :param target_position:     目标此刻的定位坐标
    :return:    被选择的三个小车
    """
    selected_car = []
    distance_map = dict()
    for num, car in car_map.items():
        distance = math.sqrt((car.position[0] - target_position[0]) ** 2 + (car.position[1] - target_position[1]) ** 2)
        distance_map[distance] = car
    sorted_dis = sorted(distance_map)
    selected_car.append(distance_map[sorted_dis[0]])
    selected_car.append(distance_map[sorted_dis[1]])
    selected_car.append(distance_map[sorted_dis[2]])

    return selected_car


def cmd_test(car, i):
    if i == 0:
        msgs = get_control("w")   # v, w, g , rty
    elif i == 1:
        msgs = get_control("t")
    elif i == 2:
        msgs = get_control("y")

    for msg in msgs:
        car.send(msg)
        time.sleep(0.2)
    info = "Action：左转"
    time_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return "{0}：{1}".format(time_string, info)


