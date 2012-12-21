import collections
import threading
import time

candle = collections.deque(xrange(5))

def burun(direction, nextSource):
    while True:
        try: next = nextSource()
        except IndexError: break
        else: print "%8s: %s" % (direction, next)
        time.sleep(0.1)
    print '%8s done' % direction
    return

left = threading.Thread(target=burun, args = ('Left', candle.popleft))
right = threading.Thread(target = burun, args = ("Right", candle.pop))

left.start()
right.start()

left.join()
right.join()
