# -*- coding utf-8 -*-
# @Time : 2021/1/4 16:29
# @Author : DH
# @File : test.py.py
# @Software : PyCharm
import math
from car_control import *
from gps_transform import gps_transform
from car_control import *

size = len(defined_control)
for _ in range(20):
    if len(defined_control) > 0:
        cmd = defined_control.pop()
    else:
        cmd = 's'
    print(cmd)
    print(defined_control)


