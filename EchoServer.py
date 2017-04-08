
import socket,traceback
from threading import *
import time
from builtins import KeyboardInterrupt
import threading
import sys

host = '127.0.0.1'
port = 51423
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

def clientThread(client,addr):
    client.send(b"Welcome to the server.")
    while True:
        data = client.recv(1024)
        time.sleep(1)
        if not data:
            break
        client.sendall(" %s:%s say:%s" %(addr[0],str(addr[1]),data))
        print('%s:%s say:%s'% (addr[0],str(addr[1]),data))

    client.close()
try:
    s.bind((host,port))
except socket.error as msg:
    print('Bind failed.Error code:%s Message %s' %(str(msg[0],str(msg[1]))))
    sys.exit()
s.listen(1)


while True:
    client,addr = s.accept()
    print('Connected with %s : %s ' %(addr[0],str(addr[1])))
    t = threading.Thread(target=clientThread,args=(client,addr))
    t.start()
s.close()