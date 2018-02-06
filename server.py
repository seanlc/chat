import socket
import select

def send_msg(msg):
  for cn in conns:
      cn.send(msg)


s = socket.socket()
print("socket created")

port = 4188

s.bind(('', port))

s.listen(2)

inputs = [s]
conns = []

while True:
    iRdy, oRdy, err = select.select(inputs, [], [])
    for sock in iRdy:
        if sock == s:
            # new connection
            c, addr = sock.accept()
            print('Got connection from', addr)
            inputs.append(c)
            msg = str(addr) + " has joined the chat room"
            conns.append(c)
            send_msg(msg.encode())
        else:
            msg = sock.recv(4196)
            if len(msg) > 0:
                send_msg(msg)
            else:
                conns.remove(sock)
                inputs.remove(sock)
                c.close()

#    c.close()
