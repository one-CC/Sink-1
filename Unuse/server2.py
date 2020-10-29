# -*- coding: utf-8 -*-
# @Time : 2020/7/9 18:50
# @Author : DH
# @Site :
# @File : server.py
# @Software: PyCharm
""""
    基于线程池的方式设计的服务器
    有最大连接限制，超过限制不能接收消息
"""
import socket
import threading
import concurrent.futures as futures
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 6666
i = 0
ex = futures.ThreadPoolExecutor(max_workers=99)   # 超过则排队


def receive(socket_exp):
    global i, lock
    try:
        while True:
            data = socket_exp.recv(1024)
            if not data:
                break
            print("收到消息啦：{}".format(data.decode('utf-8')))
    except ConnectionResetError as CR:
        pass
    finally:
        lock.acquire()
        print("第{}个tcp连接已断开！".format(i))
        i = i - 1
        thread_list.pop(i)
        print("当前活跃的线程数：" + str(len(thread_list)))
        lock.release()


server.bind((host, port))
server.listen(3)  # n线程的服务器可允许的最大socket连接数为n+num，超过后就排队
thread_list = []
lock = threading.Lock()

while True:
    try:
        print("等待连接中...")
        while True:
            client, addr = server.accept()
            if client:
                i += 1
                ex.submit(receive, client)
                thread_list.append(client)
                break
    except:
        print("连接数超啦！！！")
    else:
        print("第{0}个访问者来啦！它是'{1}'".format(i, str(addr[0])))
        send_msg = "欢迎访问浩gg，" + str(addr[0]) + '！'
        buffersize = client.send(send_msg.encode('utf-8'))
        print("发送了{0}个比特过去".format(buffersize))
        print("当前活跃的线程：" + str(thread_list))
