#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   cold
#   E-mail  :   wh_linux@126.com
#   Date    :   12/12/14 09:12:12
#   Desc    :   Python select echo server
#

import select
import socket
import sys
import Queue

# 建立TCP/IP 连接
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置非阻塞
server.setblocking(0)

server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
# 建立连接
server.bind(server_address)

# 监听5个客户端连接
server.listen(5)

# 将连接加入到接收监视列表,初始化发送监视列表和消息队列
inputs = [ server ]
outputs = []
message_queues = {}

# 开启主程序循环
while inputs:
    print >>sys.stderr, 'waiting for the next event'
    # 使用select阻塞
    # select 接收3个参数: 接收列表(inputs) 发送列表(outputs)
    # 和错误列表(inputs), select分别对这三个列表进行监听
    # 当接收了inputs里面监听连接的请求会将socket放入readable里
    # 当可以发送时会将socket放入writeable,
    # 当监听的连接发送错误时会将socket放入exceptional,并将这三个
    # 列表返回
    readable, writeable, exceptional = select.select(inputs,
                                                     outputs,
                                                     inputs)

    # 读取收到的数据
    for s in readable:
        # 如果是主服务器套接字,则说明是客户端来建立连接
        if s is server:
            # 建立客户端连接
            connection, client_address = s.accept()
            print >>sys.stderr, '  connection from', client_address
            # 设置客户端连接非阻塞
            connection.setblocking(0)
            # 将客户端连接键入到接收监视列表
            inputs.append(connection)
            # 初始化客户端消息队列
            message_queues[connection] = Queue.Queue()
        else: # 如果不是主服务器套接字则说明客户端连接已建立,并且已经发送了数据
            # 读取客户端发送的数据
            data = s.recv(1024)
            if data:
                print >>sys.stderr, ' received "%s" from %s' % (data, s.getpeername())
                # 将发送来的数据放到消息队列
                message_queues[s].put(data)
                # 如果当前连接不在发送监视列表则加入
                if s not in outputs: outputs.append(s)
            else: # 若过没有可读套接字, 说明来自已断开连接的客户
                print >>sys.stderr, ' closing', client_address
                # 移除发送/接收监视列表并关闭连接,清除消息队列
                if s in outputs: outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]
    # 读取发送的数据,并读取消息队列,发送消息
    for s in writeable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            print >>sys.stderr, '  ', s.getpeername(), 'queue empty'
            outputs.remove(s)
        else:
            print >>sys.stderr, '  sending "%s" to %s' % (next_msg, s.getpeername())
            s.send(next_msg)

    for s in exceptional:
        print >>sys.stderr, 'exception condition on', s.getpeername()
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]
