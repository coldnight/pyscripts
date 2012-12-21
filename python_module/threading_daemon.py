#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author : Palimz
# E-mail : wh_linux@126.com
# Date   : 12-11-23 下午2:46
#
import threading
import time
import logging

logging.basicConfig(level = logging.DEBUG, format = '[%(levelname)s] (%(threadName)-10s) %(message)s')

def daemon():
    logging.debug("Starting")
    time.sleep(2)
    logging.debug("Exiting")

d = threading.Thread(name="daemon", target=daemon)
d.setDaemon(True)

def non_daemon():
    logging.debug("Starting")
    logging.debug("Exiting")

t = threading.Thread(name="non-daemon", target=non_daemon)

d.start()
t.start()
d.join(1)
print 'd.isAlive()', d.isAlive()
