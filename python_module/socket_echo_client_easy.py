import socket
import sys

def get_contants(prefix):
    """Create a dictionary mapping socket module"""
    return dict((getattr(socket, n), n) for n in dir(socket) if n.startswith(prefix))

families = get_contants('AF_')
types = get_contants('SOCK_')
protocols = get_contants("IPPROTO_")

sock = socket.create_connection(('localhost', 10000))
print >>sys.stderr, 'Family     :', families[sock.family]
print >>sys.stderr, 'Type       :', types[sock.type]
print >>sys.stderr, 'Protocol   :', protocols[sock.proto]

try:
    # Send data
    message = 'This is the message. It will be repeated.'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
