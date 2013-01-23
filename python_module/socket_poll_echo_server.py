#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   wh
#   E-mail  :   wh_linux@126.com
#   Date    :   13/01/06 09:53:13
#   Desc    :
#

import select
import socket
import sys
import Queue


def print_msg(msg, *args):
    msg = msg % args if args else msg
    print >>sys.stderr, msg

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置socket非阻塞
server.setblocking(0)

server_address = ('localhost', 10000)
print_msg('starting up on %s port %s', *server_address)
server.bind(server_address)

server.listen(5)
# 初始化消息队列和超时时间
message_queues = {}
TIMEOUT = 1000 # 1s
# poll event:
# POLLIN    输入准备就绪          00000001 1
# POLLPRI   优先级输入准备就绪    00000010 2
# POLLOUT   能够接收输出          00000100 4
# POLLERR   错误                  00001000 8
# POLLHUP   通道关闭              00010000 16
# POLLNVAL  通道未打开            00100000 32

# 定义只读和读写事件
READ_ONLY = ( select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR )
READ_WRITE = READ_ONLY | select.POLLOUT

# 获取poll并注册当前服务
poller = select.poll()
poller.register(server, READ_ONLY)

# 初始化文件描述符到socket的映射
fd_to_socket = { server.fileno():server }

while True:
    print_msg('waiting for the next event')
    # 调用poll事件,返回socket文件描述父和事件标志的元组
    events = poller.poll(TIMEOUT)

    for fd, flag in events:
        # 根据socket文件描述符在映射中找到socket
        s = fd_to_socket[fd]
        # 输入事件处理
        if flag & (select.POLLIN | select.POLLPRI):
            # 如果socket是当前socket则是客户建立连接
            if s is server:
                # 获取连接,并设置非阻塞,加入文件描述符到socket的映射
                connection, client_address = s.accept()
                print_msg('  connection %s', client_address)
                connection.setblocking(0)
                fd_to_socket[ connection.fileno() ] = connection
                # 注册poll只读事件
                poller.register(connection, READ_ONLY)
                # 初始化客户连接消息队列
                message_queues[connection] = Queue.Queue()
            else:  # 如果不是当前socket则说明已和客户建立连接,并可以接收数据
                data = s.recv(1024)  # 接收数据
                # 如果有数据则将数据加入到消息队列
                if data:
                    print_msg('  received "%s" from %s', data, s.getpeername())
                    message_queues[s].put(data)
                    # 并更poll注册事件为读写事件
                    poller.modify(s, READ_WRITE)
                else: # 如果没数据则表示客户要断开连接
                    print_msg('  closing %s', client_address)
                    # 取消客户连接的poll监听,并关闭连接清除连接的消息队列
                    poller.unregister(s)
                    s.close()
                    del message_queues[s]
        elif flag & select.POLLHUP: # 事件是挂起则取消poll监听,管理连接
            print_msg('  closing %s HUP', client_address)
            poller.unregister(s)
            s.close()
        elif flag & select.POLLOUT: # 如果能接收输出则读取当前连接队列的消息,并发送
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                # 如果队列为空则更改客户连接poll监听时间爱能为只读
                print_msg('%s queue empty', s.getpeername())
                poller.modify(s, READ_ONLY)
            else:
                print_msg('  sending "%s" to %s', next_msg, s.getpeername())
                s.send(next_msg)
        elif flag & select.POLLERR: # 出错则取消监听关闭连接清除消息队列
            print_msg(' exception on %s', s.getpeername())
            poller.unregister(s)
            s.close()

            del message_queues[s]
