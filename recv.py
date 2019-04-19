from socket import socket, AF_INET, SOCK_DGRAM
import sys


sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('192.168.1.{}'.format(sys.argv[1]), 19001))
while True:
    try:
        data, sender = sock.recvfrom(1024)
    except KeyboardInterrupt:
        break
    msg = data.decode()
    print('{0}: {1}'.format(sender[0], msg))
sock.close()
