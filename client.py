import socket
import sys
import select
import signal

def sig_handler(signal, frame):
    print("Exit signal received")
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)

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

userName = sys.argv[1]

#TODO send username here
s.send(userName.encode())

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
            if len(msg) > 0:
                print(str(msg.decode()))
            else:
                print("server diconnected")
                s.close()
                running = 0
        elif ele == sys.stdin:
            msg = input()
            outboundMsg = userName + ": " + msg 
            s.send(outboundMsg.encode())
