#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# epoll 服务框架
#
# Author : wh
# E-mail : wh_linux@126.com
#
#
import socket
import select
import Queue
import logging

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s')


class epollServer:
    # 初始化只读和读写事件
    READ_ONLY = (select.EPOLLIN | select.EPOLLPRI | select.EPOLLHUP |
                 select.EPOLLERR |select.EPOLLET)
    READ_WRITE = READ_ONLY | select.EPOLLOUT
    def __init__(self, address = 'localhost', port=10000):
        self.epoll = select.epoll()
        self.init()
        self.message_queues = {}         # 消息队列
        self.fd_to_socket = {}           # 文件描述符到socket映射
        self.logger = logging.getLogger('Server')
        self.address = address
        self.port = port
        self.server = None
        self.client_adress = None

        return

    def init(self): pass

    def register_read(self, conn):
        """ 将连接注册到只读事件,并加入到文件描述符映射 """
        fn = conn.fileno()
        # 如果连接存在则更改,否则则注册,并加入映射
        if fn in self.fd_to_socket:
            self.epoll.modify(fn, self.READ_ONLY)
        else:
            self.fd_to_socket[fn] = conn
            self.epoll.register(conn.fileno(), self.READ_ONLY)

        return

    def register_write(self, conn):
        """ 将连接注册到读写事件, 并加入到映射 """
        fn = conn.fileno()
        if fn in self.fd_to_socket:
            self.epoll.modify(fn, self.READ_WRITE)
        else:
            self.epoll.register(conn.fileno(), self.READ_WRITE)
            self.fd_to_socket[fn] = conn

        return

    def unregister(self, conn, clear = True):
        """ 取消监听连接, clear为True时清理此连接 """
        fd = conn.fileno()
        self.logger.info('closing %s', conn.getpeername())
        self.epoll.unregister(fd)
        conn.close()
        if clear:
            del self.message_queues[conn]  # 清空消息队列
            self.fd_to_socket.pop(fd)      # 清除映射
        return

    def handle_read(self, s):
        """ 处理收到客户连接事件, 接收数据和建立连接 """
        # 如果是当前连接说明是客户来建立连接
        if s is self.server:
            connection, self.client_address = s.accept()
            self.logger.debug('  connect from %s', self.client_address)
            connection.setblocking(0)   # 设置非阻塞
            self.register_read(connection) # 注册到只读监听事件
            self.message_queues[connection] = Queue.Queue()
        else:  # 如果不是则是数据到达
            data = self.handle_data(s)
            if data:
                self.logger.debug('  received "%s" from %s', data, s.getpeername())
                # 如果有数据则将数据加入到消息队列
                # 并且修改当前连接为读写事件
                self.message_queues[s].put(data)
                self.register_write(s)
            else:
                self.logger.debug('  closing by %s', self.client_address)
                self.unregister(s)

    def handle_write(self, s):
        """ 处理发送事件, 给客户端发送消息 """
        try:
            next_msg = self.message_queues[s].get_nowait()
        except Queue.Empty:
            self.logger.debug('%s queue empty', s.getpeername())
            self.register_read(s)
        else:
            self.logger.debug('  sending "%s" to %s', next_msg, s.getpeername())
            s.send('xxx')

    def handle_err(self, s):
        """ 处理错误事件 """
        self.logger.debug(' exception on %s', s.getpeername())
        self.unregister(s)

    def handle_hup(self, s):
        """ 处理挂起事件 """
        self.logger.debug(' closing %s HUP', self.client_address)
        self.unregister(s, False)

    def handle_data(self, conn):
        """ 处理客户数据 """
        d = self.read_data(conn)
        if d.strip() in ['bye', 'quit', 'q']:
            return False
        else:
            return d

    def read_data(self, conn):
        """ 循环读取消息, 以便全部接收客户消息 """
        data = ''
        while True:
            try:
                data += conn.recv(1024)
            except socket.error:
                break
        return data

    def get_conn(self, fd):
        """ 从文件描述符中获取连接 """
        return self.fd_to_socket[fd]

    def init_server(self):
        """ 初始化服务端 """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)   # 设置非阻塞
        server_address = (self.address, self.port)
        self.logger.info('server starting up %s on port %s', *server_address)
        self.server.bind(server_address)
        self.server.listen(5)
        self.register_read(self.server)

        return

    def start(self):
        self.init_server()
        while True:
            self.logger.info('wating for event')
            # 使用epoll阻塞返回一个文件描述符和事件的元组列表
            events = self.epoll.poll()
            for fd, flag in events:
                s = self.get_conn(fd)
                # 触发读事件
                if flag & (select.EPOLLIN | select.EPOLLPRI | select.EPOLLET):
                    self.handle_read(s)
                elif flag & (select.EPOLLOUT|select.EPOLLET):
                    # 触发写发送事件
                    self.handle_write(s)
                elif flag & (select.EPOLLERR | select.EPOLLET):
                    # 连接错误
                    self.handle_err(s)
                elif flag & (select.EPOLLHUP | select.EPOLLET):
                    self.handle_hup(s)

        return

if __name__ == '__main__':
    es = epollServer()
    es.start()
