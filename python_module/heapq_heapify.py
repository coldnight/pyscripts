#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author : Palimz
# E-mail : wh_linux@126.com
# Date   : 12-11-23 上午11:33
#

import heapq
from heapq_showtree import show_tree
from heapq_heapqdata import data

print 'random     :', data
heapq.heapify(data)
print 'heapified: '
show_tree(data)