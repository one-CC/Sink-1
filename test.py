# -*- coding utf-8 -*-
# @Time : 2021/1/4 16:29
# @Author : DH
# @File : test.py.py
# @Software : PyCharm
import math
from car_control import calculate_angle
from gps_transform import gps_transform

target_gps = [103.92928882917865, 30.75245796847024]
car_gps = [103.93066708679817, 30.752462578567716]
car_angle = [-1.02722, 0.50537, 71.30127]


target_position = gps_transform(target_gps)
car_position = gps_transform(car_gps)

vector = [target_position[0] - car_position[0], target_position[1] - car_position[1]]
distance = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
angle = calculate_angle(vector)

projected_car_direction = [math.cos(car_angle[0]), math.cos(car_angle[1])]
projected_car_angle = calculate_angle(projected_car_direction)
angle_diff = projected_car_angle - angle

print("target_position: ", target_position)
print("car_position: ", car_position)
print("位置向量的角度：", angle)
print("位置向量的距离：", distance)
print("朝向向量的角度：", projected_car_angle)
print("角度差：", angle_diff)



