#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author : Palimz
# E-mail : wh_linux@126.com
# Date   : 12-11-23 下午2:53
#
import random
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] [%(threadName)-10s] %(message)s")

def worker():
    t = threading.currentThread()
    pause = random.randint(1, 5)
    logging.debug('sleepping %s', pause)
    time.sleep(pause)
    logging.debug('ending')

for i in range(3):
    t = threading.Thread(target=worker)
    t.setDaemon(True)
    t.start()
main_thread = threading.currentThread()

for t in threading.enumerate():
    if t is main_thread:
        continue
    logging.debug('joining %s', t.getName())
    t.join()