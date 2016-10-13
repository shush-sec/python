import socket

socket.setdefaulttimeout(20)
s = socket.socket()
s.connect(("www.xiaoshuwu.net",80))

ans = s.recv(1024)
#print(ans)
