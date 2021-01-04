# -*- coding: utf-8 -*-
# @Time : 2020/7/9 18:50
# @Author : DH
# @Site : 
# @File : client.py
# @Software: PyCharm
import socket
import time
import numpy as np
import threading
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
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
        for _ in range(1, 100000):
            time.sleep(0.2)
            send_msg = str(np.random.randint(1, 6)) + '#'
            client.send(send_msg.encode('utf-8'))
        print("done!")
        break
client.close()
