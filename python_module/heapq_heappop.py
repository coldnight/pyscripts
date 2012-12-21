#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author : Palimz
# E-mail : wh_linux@126.com
# Date   : 12-11-23 下午12:46
#
import heapq
from heapq_showtree import show_tree
from heapq_heapqdata import data
print 'random:', data
heapq.heapify(data)
print 'data:', data
print 'headpified:'
show_tree(data)
print
for i in xrange(2):
    smalltest = heapq.heappop(data)
    print 'pop    %3d' % smalltest
    show_tree(data)