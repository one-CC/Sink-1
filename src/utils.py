# -*- coding utf-8 -*-
# @Time : 2021/8/18 16:27
# @Author : donghao
# @File : utils.py
# @Desc : 一些简单的函数工具
import os
import asyncio


def all_uwbs_connected(uwb_map):
    """ 判断是否所有的UWB都已经连接上 """
    for uwb in uwb_map.values():
        if not uwb.connected:
            return False
    return True

def all_cars_connected(car_map=None, car_list=None):
    """ 判断是否所有的小车都已经连接上 """
    if car_map is not None:
        for car in car_map.values():
            if not car.connected or car.gps is None:
                return False
    if car_list is not None:
        for car in car_list:
            if not car.connected or car.gps is None:
                return False
    return True

def get_root_path():
    """ 获取项目根目录 """
    current_path = os.path.abspath(os.path.dirname(__file__))
    return current_path[:current_path.find("Sink") + len("Sink")]

def all_tasks_done():
    """ 判断是否所有Task都完成 """
    for t in asyncio.Task.all_tasks():
        if not t.done():
            return False
    return True