import socket

socket.setdefaulttimeout(20)
s = socket.socket()
s.connect(("www.baidu.com",80))

ans = s.recv(1024)
print(ans)
