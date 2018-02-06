import socket
import select
import signal
import sys

def send_msg(msg):
  for cn in conns:
      cn.send(msg)

def sig_handler(signal, frame):
    print("exit signal received")
    for cn in conns:
      cn.close()
    s.close()
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)

s = socket.socket()
print("socket created")

port = 4188

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))

s.listen(2)

inputs = [s]
conns = []
nameMappings = {}

while True:
    iRdy, oRdy, err = select.select(inputs, [], [])
    for sock in iRdy:
        if sock == s:
            # new connection
            c, addr = sock.accept()
            print('Got connection from', addr)
            
            inputs.append(c)
            userName = c.recv(4196)
            nameMappings[c] = userName.decode()
            conns.append(c)
            
            msg = str(userName.decode()) + " has joined the chat room"
            send_msg(msg.encode())
        else:
            msg = sock.recv(4196)
            if len(msg) > 0:
                send_msg(msg)
            else:
                conns.remove(sock)

                inputs.remove(sock)

                msg = str(nameMappings[sock]) + " has disconnected"
                send_msg(msg.encode())

                sock.close()

