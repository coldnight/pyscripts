#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author : Palimz
# E-mail : wh_linux@126.com
# Date   : 12-11-23 下午3:03
#
import threading
import logging

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] [%(threadName)-10s] %(message)s")


class MyThreadWithArgs(threading.Thread):
    def __init__(self, group=None, target = None, name = None,
                  args = (), kwargs = None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name = name, verbose = verbose)
        self.args = args
        self.kwargs = kwargs
        return

    def run(self):
        logging.debug("runniing with %s and %s", self.args, self.kwargs)
        return

for i in range(5):
    t = MyThreadWithArgs(args= (i,), kwargs = {'a':'A', 'b':'B'})
    t.start()
