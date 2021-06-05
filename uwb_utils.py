# -*- coding utf-8 -*-
# @Time : 2021/6/5 15:08
# @Author : DH
# @File : uwb_utils.py
# @Software : PyCharm


def is_all_uwbs_connected(uwb_map):
    return uwb_map[1].connected and uwb_map[2].connected and uwb_map[3].connected


