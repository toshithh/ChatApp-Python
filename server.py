import socket
import threading
import time

class Peer2Peer:
    def recv(self, c):
        try:
            n = int(float(c.recv(12).decode())) #Recv
        except:
            return("None")
        msg = c.recv(n).decode()            #Receive
        #time.sleep(0.001)
        c.sendall("ack".encode())           #Send
        return msg

    def send(self, c, msg):
        msg = str(msg)
        n = str(len(msg))
        i = 11-len(n)
        n = f"%.{i}f" % len(msg)
        c.sendall(n.encode())       #Send
        #time.sleep(0.01)
        c.sendall(msg.encode())     #Send
        msg = c.recv(3)             #recv
        if msg:
            return 1
    

class Server(Peer2Peer):
    def __init__(self, ip="127.0.0.1", port=6969):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.socket.bind((ip, port))
        self.socket.listen(50)
        self.__lock_msg = threading.Lock()
        self.__lock_addrs = threading.Lock()
        self.addrs = []
        self.messages = []
        self.exit = False
        self.connections()
    
    def client(self, c, addr):
        self.__lock_addrs.acquire()
        if addr not in self.addrs:
            self.addrs.append(addr)
        self.__lock_addrs.release()
        try:
            while True:
                msg = eval(self.recv(c))
                if msg:
                    self.__lock_msg.acquire()
                    msg.insert(1, str(addr))
                    print(msg)
                    self.messages.append(msg)#
                    print(self.messages)
                    self.__lock_msg.release()
        #############################
                data = {
                    "addr": self.addrs,
                }
                self.__lock_msg.acquire()
                for i in range(len(self.messages)):
                    if str(self.messages[i][0]) == str(addr):
                        temp = self.messages.pop(i)
                        data[temp[1]] = temp[2]
                        i-=1
                self.__lock_msg.release()
                self.send(c, data)
        except ConnectionError as e:
            print(e)
            self.__lock_addrs.acquire()
            try:
                self.addrs.remove(addr)
            except:
                print(self.addrs, addr)
            self.__lock_addrs.release()
            return 0

    
    def connections(self):
        while True:
            c, addr = self.socket.accept()
            threading.Thread(target = self.client, args=(c, addr)).start()
            if self.exit:   self.socket.close()


if __name__ == "__main__":
    test = Server()
    def t():
        time.sleep(7)
        test.exit = True
    threading.Thread(target = t, args=()).start()