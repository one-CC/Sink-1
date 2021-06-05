# -*- coding: utf-8 -*-
# @Time : 2020/7/9 18:50
# @Author : DH
# @Site :
# @File : client.py
# @Software: PyCharm
import socket
import time
import threading
import concurrent.futures as futures
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 6666
connected = False


def receive(socket_exp):
    try:
        while True:
            data = socket_exp.recv(1024)
            if not data:
                break
            print("收到消息啦：{}".format(data.decode('utf-8')))
    except ConnectionAbortedError as CAE:
        pass
    finally:
        print("断开连接了！！！")


ex = futures.ThreadPoolExecutor(max_workers=2)


while True:
    try:
        if not connected:
            client.connect((host, port))
    except:
        print("连接失败啦...")
        pass
    else:
        if not connected:
            print("连接成功啦！")
            connected = True
            ex.submit(receive, client)
        send_msg = input("输入要发送的消息：")
        if send_msg == 'quit':
            break
        client.send(send_msg.encode('utf-8'))
time.sleep(5)
client.close()