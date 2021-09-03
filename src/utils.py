# -*- coding utf-8 -*-
# @Time : 2021/8/18 16:27
# @Author : donghao
# @File : utils.py
# @Desc : 一些简单的函数工具
import os
from src.models import Car, UWB
from typing import Dict


def all_uwbs_connected(uwb_map: Dict[int, UWB]):
    """ 判断是否所有的UWB都已经连接上 """
    for uwb in uwb_map.values():
        if not uwb.connected:
            return False
    return True

def all_cars_connected(car_map: Dict[int, Car]):
    """ 判断是否所有的小车都已经连接上 """
    for car in car_map.values():
        if not car.connected:
            return False
    return True

def get_root_path():
    current_path = os.path.abspath(os.path.dirname(__file__))
    return current_path[:current_path.find("server") + len("server")]
