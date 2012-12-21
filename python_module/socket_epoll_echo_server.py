#!/usr/bin/env python
#-*- coding:utf-8 -*-
import socket
import select
import Queue
import logging
from util import print_msg

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')

# 建立socket,并建立连接监听5个客户连接
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)   # 设置非阻塞
server_address = ('localhost', 10000)
print_msg('server starting up %s on port %s', *server_address)
server.bind(server_address)
server.listen(5)

# 初始化连接消息队列
message_queues = {}

# 建立epoll只读和读写事件并将当前服务socket注册监听只读事件
# epoll events:
# EPOLLIN      连接到达或有数据来临
# EPOLLPRI     优先级的连接或数据到达
# EPOLLOUT     有数据要写(发送)
# EPOLLERR     连接发生错误
# EPOLLET      边缘触发模式 仅支持非阻塞模式
# EPOLLHUP     连接关闭
# EPOLLNVAL    连接未打开
READ_ONLY = (select.EPOLLIN | select.EPOLLPRI | select.EPOLLHUP | select.EPOLLERR |select.EPOLLET)
READ_WRITE = READ_ONLY | select.EPOLLOUT
epoll = select.epoll()
epoll.register(server.fileno(), READ_ONLY)

# 初始化文件表述符到socket的映射
fd_to_sock = {server.fileno():server}

# 开始主循环
while True:
    print_msg('wating for event')
    # 使用epoll阻塞返回一个文件描述符和事件的元组列表
    events = epoll.poll()

    for fd, flag in events:
        s = fd_to_sock[fd]
        # 触发读事件
        if flag & (select.EPOLLIN | select.EPOLLPRI | select.EPOLLET):
            # 如果是当前连接说明是客户来建立连接
            if s is server:
                connection, client_address = s.accept()
                print_msg('  connect from %s', client_address)
                connection.setblocking(0)   # 设置非阻塞
                fd_to_sock[connection.fileno()] = connection # 将连接加入映射
                epoll.register(connection.fileno(), READ_ONLY) # 注册到只读监听事件
                message_queues[connection] = Queue.Queue()
            else:  # 如果不是则是数据到达
                data = s.recv(1024)
                if data:
                    print_msg('  received "%s" from %s', data, s.getpeername())
                    # 如果有数据则将数据加入到消息队列
                    # 并且修改当前连接为读写事件
                    message_queues[s].put(data)
                    epoll.modify(s.fileno(), READ_WRITE)
                else:
                    print_msg('  closing by %s', client_address)
                    # 如果没有数据则说明是断开连接
                    # 清空消息队列,取消epoll事件监听,关闭连接
                    epoll.unregister(s.fileno())
                    s.close()
                    del message_queues[s]
        elif flag & (select.EPOLLOUT|select.EPOLLET):
            # 触发写发送事件
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                print_msg('%s queue empty', s.getpeername())
                epoll.modify(s.fileno(), READ_ONLY)
            else:
                print_msg('  sending "%s" to %s', next_msg, s.getpeername())
                s.send(next_msg)
        elif flag & (select.EPOLLERR | select.EPOLLET):
            # 连接错误
            print_msg(' exception on %s', s.getpeername())
            epoll.unregister(s.fileno())
            s.close()
            del message_queues[s]
        elif flag & (select.EPOLLHUP | select.EPOLLET):
            print_msg(' closing %s HUP', client_address)
            epoll.unregister(s.fileno())
            s.close()
