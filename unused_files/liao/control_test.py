#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-12-31 11:22
# @Author  : lynch

from socket import *
import concurrent.futures as futures
import time


class TCPClient:
    def __init__(self, host='192.168.50.1', port=8888):
        self.HOST = host
        self.PORT = port
        self.BUFSIZ = 1024
        self.ADDRESS = (self.HOST, self.PORT)
        self.tcpClientSocket = socket(AF_INET, SOCK_STREAM)
        self.tcpClientSocket.connect(self.ADDRESS)

    def send(self, msg):
        """
        向服务器端发送信息
        :param msg:
        :return:
        """
        self.tcpClientSocket.send(msg.encode('utf-8'))

    def receive(self):
        try:
            while True:
                data = self.tcpClientSocket.recv(self.BUFSIZ)
                if not data:
                    break
                print("接收到服务器端消息：{}".format(data.decode('utf-8')))
        finally:
            print("tcp连接已断开！")
            self.tcpClientSocket.close()


def main():
    ex = futures.ThreadPoolExecutor(max_workers=1)
    tc = TCPClient()
    ex.submit(tc.receive)
    # 前 前 后 左 停
    data = ['$1,0,0,0,0,0,0,0,0#', '$1,0,0,0,0,0,0,0,0#', '$2,0,0,0,0,0,0,0,0#', '$3,0,0,0,0,0,0,0,0#',
            '$0,0,0,0,0,0,0,0,0#']
    data0 = ['$0,0,0,0,0,0,1,0,0#', '$0,0,0,0,0,0,8,0,0#']  # 灯开关
    data2 = ['$0,0,0,0,1,0,0,0,0#', '$0,0,0,0,0,0,0,0,1#', '$0,0,0,0,2,0,0,0,0#']  # 超声波控制
    for d in data2:
        tc.send(d)
        time.sleep(2)
    tc.tcpClientSocket.close()


if __name__ == '__main__':
    main()
