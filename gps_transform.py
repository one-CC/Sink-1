# -*- coding: utf-8 -*-
# @Time : 2020/10/26 17:48
# @Author : DH
# @Site : 
# @File : gps_transform.py
# @Software: PyCharm
import math
from pyproj import CRS, Transformer
# 48:102E~108E;   49:108E~114E
# 每个经度投影带，中央经度为500 000米，东加西减；
# 326xx:北半球;  327xx:南半球
# 对北半球，赤道为0米，北加南减；对南半球，赤道为10 000 000米，北加南减；
# 成都：104.07E,30.67W
crs = CRS.from_epsg(4326)
crs_cs = CRS.from_epsg(32648)
transformer = Transformer.from_crs(crs, crs_cs)


def gps_transform(gps):
    loc = list(transformer.transform(gps[1], gps[0]))
    loc[0] = round(loc[0], 2)
    loc[1] = round(loc[1], 2)
    return loc


if __name__ == '__main__':
    p0 = gps_transform([103.92388, 30.74216])
    p1 = gps_transform([103.93755, 30.75348])
    area_x = [p0[0], p1[0]]
    area_y = [p0[1], p1[1]]
    print(area_x)
    print(area_y)
    # gps1 = [103.92972, 30.75184]
    # gps2 = [103.92977, 30.75151]
    # pos1 = gps_transform(gps1)
    # pos2 = gps_transform(gps2)
    # print('GPS[103.92972, 30.75184]由UTM转化为直角坐标:', pos1)
    # print('GPS[103.92977, 30.75151]由UTM转化为直角坐标:', pos2)
    # print('两个点的直线距离为：', math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2))

