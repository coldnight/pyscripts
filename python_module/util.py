import sys

def print_msg(msg, *args):
    msg = msg % args if args else msg
    print >>sys.stderr, msg
