#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author : Palimz
# E-mail : wh_linux@126.com
# Date   : 12-11-23 下午1:24
#
import bisect
import random

random.seed(1)

print 'New    Pos    Contents'
print '---    ---    --------'
l = []
for i in range(1, 15):
    r = random.randint(1, 100)
    position = bisect.bisect(l, r)
    bisect.insort(l, r)
    print '%3d    %3d' % (r, position), l
