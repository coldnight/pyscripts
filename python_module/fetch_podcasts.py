#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author : Palimz
# E-mail : wh_linux@126.com
# Date   : 12-11-23 下午1:42
#
from Queue import Queue
from threading import Thread
import time
import urllib
import urlparse

import feedparser

nume_fetch_threads = 2
enclosure_queue = Queue()

feed_urls = ['http://advocacy.python.org/podcasts/littlebit.rss',]

def downloadEnclosures(i, q):
    while True:
        print '%s: Looking for the next enclosure' % i
        url = q.get()
        parsed_url = urlparse.urlparse(url)
        print '%s: Downloading:' % i, parsed_url.path
        response = urllib.urlopen(url)
        data = response.read()
        outfile_name = url.rpartition('/')[-1]
        with open(outfile_name, 'wb') as outfile:
            outfile.write(data)
        q.task_done()

for i in range(nume_fetch_threads):
    worker = Thread(target= downloadEnclosures, args = (i, enclosure_queue,))
    worker.setDaemon(True)
    worker.start()

for url in feed_urls:
    response = feedparser.parse(url, agent='fetch_podcasts.py')
for entry in response['entries'][-5:]:
    for enclosure in entry.get('enclosures', []):
        parsed_url = urlparse.urlparse(enclosure['url'])
        print 'Queuing:', parsed_url.path
        enclosure_queue.put(enclosure['url'])
print '*** Main thread waiting'
enclosure_queue.join()
print '*** Done'