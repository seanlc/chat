import socket
import select
import signal
import sys

class chatServer:

    def __init__(self, port = 4188):
        self.s = socket.socket()
        self.port = port
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', self.port))
        self.s.listen(5)
        self.inputs = [self.s]
        self.conns = []
        self.nameMappings = {}
        self.iRdy = []
        signal.signal(signal.SIGINT, self.sig_handler)

    def __send_msg(self, msg):
        for cn in self.conns:
            cn.send(msg)

    def sig_handler(self, signal, frame):
        print("exit signal received")
        for cn in self.conns:
            cn.close()
        self.s.close()
        sys.exit(0)

    def __existing_conn(self, sock):
    
        msg = sock.recv(4196)
        if len(msg) > 0:
            self.__send_msg(msg)
        else:
            self.conns.remove(sock)

            self.inputs.remove(sock)

            msg = str(self.nameMappings[sock]) + " has disconnected"
            self.__send_msg(msg.encode())

            sock.close()


    def __new_conn(self, sock):
        c, addr = sock.accept()
        print('Got connection from', addr)
            
        self.inputs.append(c)
        self.conns.append(c)
        userName = c.recv(4196)
        self.nameMappings[c] = userName.decode()
        msg = str(userName.decode()) + " has joined the chat room"
        self.__send_msg(msg.encode())
    

    def __get_input(self):
        self.iRdy, oRdy, err = select.select(self.inputs, [], [])        
        for sock in self.iRdy:
            if sock == self.s:
                self.__new_conn(sock)
            else:
                self.__existing_conn(sock)

    def start(self):
        while True:
            self.__get_input() 

server = chatServer()
server.start()

