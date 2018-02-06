import socket
import sys
import select

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.25)
    print("Socket created")
except socket.error as err:
    print("socket creation failed with error %s" %(err))

port = 4188


#try:
#    host_ip = socket.gethostbyname()
#except socket.gaierror:
#    print "error resolving host"
#    sys.exit()

s.connect(('' , port))

inputs = [s, sys.stdin]
outputs = []

running = 1
while running:
    try: 
        in_rdy,out_rdy, err = select.select(inputs, outputs, [])
    except socket.error as e:
        break;
    except select.error as e:
        break;

    for ele in in_rdy:
        if ele == s:
            msg = s.recv(4196)
            print("server said " + str(msg.decode()))
        elif ele == sys.stdin:
            msg = input()
            s.send(msg.encode())
#            print("sending message: " + msg)
