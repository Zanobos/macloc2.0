import socket
import struct
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 6000

FMT = "<IB3x3h1H"

for i in range(0, 200):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = struct.pack(FMT, 2001, 100, i, i, i, 1200)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(.01)
