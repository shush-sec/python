import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',51423))

while True:
    word = input(' ')
    s.sendall(word.encode())
    print(s.recv(1024))
s.close()