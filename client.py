# -*- coding: utf-8 -*-
# @Time : 2020/7/9 18:50
# @Author : DH
# @Site : 
# @File : client.py
# @Software: PyCharm
import socket
import time
import threading
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.31.66'
port = 8888
connected = False
lock = threading.Lock()


def receive(socket_exp):
    try:
        while True:
            data = socket_exp.recv(1024)
            if not data:
                break
            print("收到消息啦：{}".format(data.decode('utf-8')))
    except ConnectionAbortedError:
        pass
    except ConnectionResetError:
        pass
    finally:
        lock.acquire()
        global connected
        connected = False
        lock.release()
        print("断开连接了！！！")


thread = threading.Thread(target=receive, args=(client, ))

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
            thread.start()
        send_msg = input("输入要发送的消息：")
        if send_msg == 'q' or connected is False:
            break
        client.send(send_msg.encode('utf-8'))
client.close()
