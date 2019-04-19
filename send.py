from socket import *
import sys


sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('192.168.1.{}'.format(sys.argv[1]), 19001))
while True:
    try:
        msg = input()
    except KeyboardInterrupt:
        break
    sock.sendto(msg.encode(), ('192.168.1.{}'.format(sys.argv[2]), 19001))
sock.close()
