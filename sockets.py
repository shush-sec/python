import socket

solist = [x for x in dir(socket) if x.startswith('SO_')]
for x in solist:
    print (x )