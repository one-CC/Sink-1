# -*- coding utf-8 -*-
# @Time : 2021/7/30 14:36
# @Author : donghao
# @File : test_utils.py
# @Desc : 这个文件存放测试时可能会使用到的方法或类
import random

from history.sync_sink.models import Car
from src.car_control import get_control


#  键盘读取类
class ControlKeyboard:
    def __init__(self, keyboard_input):
        self.KEYBOARD_INPUT = keyboard_input

    def get_control(self):
        """

        :return:
        """
        msg, energy_consumption = "", 0
        cmd = self.KEYBOARD_INPUT
        # 小车方向
        if cmd == 'w':  # 前
            msg = '$1,0,0,0,0,0,0,0,0#'
            energy_consumption = 0.4
        elif cmd == 'quick':  # 快速前
            msg = '$5,0,0,0,0,0,0,0,0#'
            energy_consumption = 0.6
        elif cmd == 'slow':  # 慢速前
            msg = '$6,0,0,0,0,0,0,0,0#'
            energy_consumption = 0.2
        elif cmd == 'x':  # 后
            msg = '$2,0,0,0,0,0,0,0,0#'
            energy_consumption = 0.4
        elif cmd == 'a':  # 左
            msg = '$3,0,0,0,0,0,0,0,0#$0,0,0,0,0,0,0,0,0#'
            energy_consumption = 0.2
        elif cmd == 'd':  # 右
            msg = '$4,0,0,0,0,0,0,0,0#$0,0,0,0,0,0,0,0,0#'
            energy_consumption = 0.2
        elif cmd == 'z':  # 左转
            msg = '$0,1,0,0,0,0,0,0,0#$0,0,0,0,0,0,0,0,0#'
            energy_consumption = 0.2
        elif cmd == 'c':  # 右转
            msg = '$0,2,0,0,0,0,0,0,0#$0,0,0,0,0,0,0,0,0#'
            energy_consumption = 0.2
        elif cmd == 's':  # 停
            msg = '$0,0,0,0,0,0,0,0,0#'

            # 灯开关控制
        elif cmd == 'v':  # 开
            msg = '$0,0,0,0,0,0,1,0,0#'
        elif cmd == 'b':  # 关
            msg = '$0,0,0,0,0,0,8,0,0#'

            # 摄像头方向
        elif cmd == 'i':  # 上
            msg = '$0,0,0,0,3,0,0,0,0#'
            # msg.append('$0,0,0,0,8,0,0,0,0#')
        elif cmd == 'm':  # 下
            msg = '$0,0,0,0,4,0,0,0,0#'
            # msg.append('$0,0,0,0,8,0,0,0,0#')
        elif cmd == 'j':  # 左
            msg = '$0,0,0,0,6,0,0,0,0#'
            # msg.append('$0,0,0,0,8,0,0,0,0#')
        elif cmd == 'l':  # 右
            msg = '$0,0,0,0,7,0,0,0,0#'
            # msg.append('$0,0,0,0,8,0,0,0,0#')
        elif cmd == 'k':  # 停
            msg = '$0,0,0,0,8,0,0,0,0#'

            # 超声波控制
        elif cmd == 'r':  # 左
            msg = '$0,0,0,0,1,0,0,0,0#'
        elif cmd == 't':  # 中
            msg = '$0,0,0,0,0,0,0,0,1#'
        elif cmd == 'y':  # 右
            msg = '$0,0,0,0,2,0,0,0,0#'

        print(msg)
        print(energy_consumption)
        return msg, energy_consumption


def target_move(target: Car, randomly: bool):
    """
    控制目标移动
    :param target: 目标小车
    :param randomly: 是否随机移动
    :return:
    """
    if randomly:
        # 方法一：随机轨迹
        msgs, energy_consumption = randomly_move()
    else:
        # 方法二：自定义轨迹
        msgs, energy_consumption = defined_move()
    if msgs is None:
        return
    target.send(msgs, energy_consumption)


def randomly_move():
    # 随机轨迹，概率：6/8 1/8 1/8
    control = ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'z', 'c']
    cmd_index = random.randint(0, 11)
    cmd = control[cmd_index]
    return get_control(cmd)


# 自定义轨迹
defined_control = ['w'] * 50
def defined_move():
    msgs, energy_consumption = None, 0
    if len(defined_control) > 0:
        cmd = defined_control.pop()
        msgs, energy_consumption = get_control(cmd)
    return msgs, energy_consumption
