#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author : Palimz
# E-mail : wh_linux@126.com
# Date   : 12-11-23 下午1:29
#
import Queue

q = Queue.Queue()
for i in range(5):
    q.put(i)

while not q.empty():
    print q.get(),
print


q = Queue.LifoQueue()

for i in range(5):
    q.put(i)

while not q.empty():
    print q.get(),
print