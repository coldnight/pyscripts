#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author : Palimz
# E-mail : wh_linux@126.com
# Date   : 12-11-23 下午1:18
#
import heapq
from heapq_heapqdata import data
print 'all                :', data
print '3 largest          :', heapq.nlargest(3, data)
print 'form sort          :', list(reversed(sorted(data)[-3:]))
print '3 smallest         :', heapq.nsmallest(3, data)
print 'from sort          :', sorted(data)[:3]