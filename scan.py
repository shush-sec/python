import socket
import threading
def scan(ip,port):
    s = socket.socket()
    s.settimeout(0.1)
    if s.connect_ex((ip,port)) ==0:
        print('%s:%s OPEN'%(ip,port))
    s.close()
portlist = [80,3306,3398,3389,7070,8080,8081,8181,8888,9090]
if __name__ == '__main__':
    for j in range(1,255):
        for i in portlist:
            threads =  threading.Thread(target=scan,args=('192.168.1.'+str(j),i,)) 
            threads.start()

    
