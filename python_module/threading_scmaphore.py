import logging
import random
import threading
import time

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] [%(threadName)-10s] %(message)s")

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()

    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('Running: %s', self.active)

    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug('Running: %s', self.active)

def worker(s, pool):
    logging.debug('Waiting to join the poll')
    with s:
        name = threading.currentThread().getName()
        pool.makeActive(name)
        pool.makeInactive(name)

pool = ActivePool()
s = threading.Semaphore()
for i in range(10):
    t = threading.Thread(target = worker,
                         name = str(i),
                         args=(s, pool))
    t.start()
