#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author : Palimz
# E-mail : wh_linux@126.com
# Date   : 12-11-23 下午12:51
#
import heapq
from heapq_showtree import show_tree
from heapq_heapqdata import data
heapq.heapify(data)
print 'start:'
show_tree(data)

for n in [0, 13]:
    smalltest = heapq.heapreplace(data, n)
    print 'replace %2d with %2d:' % (smalltest, n)
    show_tree(data)