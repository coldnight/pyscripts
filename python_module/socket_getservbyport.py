import socket
import urlparse

for port in range(1, 1000):
    print urlparse.urlunparse(
        (socket.getservbyport(port), 'linuxzen.com', '/', '', '', '')
    )
