import threading
import logging

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] [%(threadName)-10s] %(message)s")

def worker_with(lock):
    with lock:
        logging.debug('Lock acquired via with')

def worker_non_with(lock):
    lock.acquire()
    try:
        logging.debug('Lock acquire directly')
    finally:
        lock.release()


lock = threading.Lock()
w = threading.Thread(target = worker_with, args = (lock,))
nw = threading.Thread(target = worker_non_with, args=(lock,))

w.start()
nw.start()
