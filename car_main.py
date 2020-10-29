# -*- coding: utf-8 -*-
# @Time : 2020/7/8 20:17
# @Author : DH
# @Site : 
# @File : car_main.py
# @Software: PyCharm
import threading
import car_video
from Unuse import AP_as_client


def watch_video():
	cv = car_video.CatchUsbVideo()
	cv.get_camera()


def control_car():
	AP_as_client.ControlShow.show_key()
	AP_as_client.main()


thread1 = threading.Thread(target=watch_video)
thread2 = threading.Thread(target=control_car)
thread1.start()
thread2.start()

