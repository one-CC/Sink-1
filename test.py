# -*- coding utf-8 -*-
# @Time : 2021/1/4 16:29
# @Author : DH
# @File : test.py.py
# @Software : PyCharm
import math
import numpy as np
import matplotlib.pyplot as plt
from gps_transform import gps_transform

fig = plt.figure()
for _ in range(100000):
    distance1 = np.random.randint(1, 10)
    distance2 = np.random.randint(1, 10)
    theta = np.arange(0, 2 * math.pi, 0.01)
    center1 = [50, 50]
    x1 = distance1 * np.cos(theta) + center1[0]
    y1 = distance1 * np.sin(theta) + center1[1]
    center2 = [55, 55]
    x2 = distance2 * np.cos(theta) + center2[0]
    y2 = distance2 * np.sin(theta) + center2[1]
    plt.ylim([0, 100])
    plt.xlim([0, 100])
    plt.plot(x1, y1, '-r', x2, y2, '--b')
    # plt.show()
    plt.pause(0.2)
    plt.cla()
# fig, ax = plt.subplots()
# y1 = []
# for i in range(50):
#     y1.append(i)
#     ax.cla()
#     ax.bar(y1, label='test', height=y1, width=0.3)
#     ax.legend()
#     plt.pause(0.3)

