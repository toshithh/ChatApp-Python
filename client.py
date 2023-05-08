import socket
import threading
import time
from server import Peer2Peer

class Client(Peer2Peer):
    def __init__(self, ip="127.0.0.1", port=6969, selfIP=socket.gethostbyname(socket.gethostname())):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        self.ip = selfIP
        self.__message = []
        self.recv_message = []
        self.exit = False
        self.lock_msg = threading.Lock()
        self.__lock_refresh = threading.Lock()
        self.__refresh = True
        threading.Thread(target=self.connect, args=()).start()

    def connect(self):
        while True:
            if self.exit == True:
                return
            self.lock_msg.acquire()
            if self.__message:
                temp = self.__message.pop(0)
                self.lock_msg.release()
                self.send(self.socket, temp)
            else:
                self.lock_msg.release()
                if not self.refresh:
                    print("Continue")
                    continue###
                self.send(self.socket, "None")
                time.sleep(0.1)
            
            rmsg = self.recv(self.socket)
            self.addr(rmsg)

    def addr(self, rmsg):
        print("Default")

    @property
    def msg(self):
        self.lock_msg.acquire()
        temp = self.__message
        self.lock_msg.release()
        return temp

    @msg.setter
    def msg(self, msg):
        self.lock_msg.acquire()
        self.__message.append(msg)
        self.lock_msg.release()

    @property
    def refresh(self):
        self.__lock_refresh.acquire()
        t = self.__refresh
        self.__lock_refresh.release()
        return t
    
    @refresh.setter
    def refresh(self, bool):
        self.__lock_refresh.acquire()
        self.__refresh = bool
        self.__lock_refresh.release()




if __name__ == "__main__":
    test = Client()
    time.sleep(3)
    test.refresh = True