import logging
import random
import threading
import time

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] [%(threadName)-10s] %(message)s")

class Counter(object):
    def __init__(self, start = 0):
        self.lock = threading.Lock()
        self.value = start
        return

    def increment(self):
        logging.debug('Waiting for lock')
        self.lock.acquire()
        try:
            logging.debug('Acquired lock')
            self.value += 1
        finally:
            self.lock.release()


def worker(c):
    for i in range(2):
        pause = random.random()
        logging.debug('sleeping %0.02f', pause)
        time.sleep(pause)
        c.increment()
    logging.debug('Done')
    return

counter = Counter()
for i in range(2):
    t = threading.Thread(target=worker, args=(counter, ))
    t.start()

logging.debug('Waiting for worker threads')
main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()
logging.debug("Counter: %d", counter.value)
