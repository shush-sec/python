import socket,traceback,time,struct
host = '127.0.0.1'
port = 51423

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))

while 1:
    try:
        message,address = s.recvfrom(8192)
        secs = int(time.time())
        secs -= 60*60*24
        secs +=2208988800
        reply = struct.pack("!I",secs)
        s.sendto(reply,address)
        print("address:%s  message: %s " % (address,message))
    except (KeyboardInterrupt,SystemError):
        raise
    except:
        traceback.print_exc()