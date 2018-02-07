import socket
import sys
import select
import signal

def sig_handler(signal, frame):
    print("Exit signal received")
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)

class chatClient:
    def __init__(self, uName, port):
    
        try:    
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(0.25)
        except socket.error as err:
            print("socket creation failed with error %s" %(err))
            sys.exit(0)
    
        self.port = port
        self.userName = uName
        self.inputs = [self.s, sys.stdin]
        self.running = 1
        self.in_rdy = []

    def __get_input(self):
        try: 
            self.in_rdy,out_rdy, err = select.select(self.inputs, [], [])
        except socket.error as e:
            pass
        except select.error as e:
            pass
    
    def __get_msg(self):        
        msg = self.s.recv(4196)
        if len(msg) > 0:
            print(str(msg.decode()))
        else:
            print("server diconnected")
            self.s.close()
            self.running = 0
    
    def __send_msg(self):        
        msg = input()
        outboundMsg = self.userName + ": " + msg 
        self.s.send(outboundMsg.encode())

    def __process_input(self):
        for ele in self.in_rdy:
            if ele == self.s:
                self.__get_msg()
            elif ele == sys.stdin:
                self.__send_msg()

    def __operate(self):
        while self.running:
            self.__get_input()
            self.__process_input()


    def connect(self):
        self.s.connect(('' , self.port))
        self.s.send(self.userName.encode())
        self.__operate()

#
#try:
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.settimeout(0.25)
#    print("Socket created")
#except socket.error as err:
#    print("socket creation failed with error %s" %(err))

client = chatClient(sys.argv[1], 4188)
client.connect()
