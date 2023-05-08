import tkinter as tk
import threading
import time
from client import Client
import socket

class Main:
    def __init__(self, w = 800, h = 480, title="Chat") -> None:
        self.client = Client_impl()#ip, port
        self.window = tk.Tk()
        self.h = h
        self.w = w
        self.msg = tk.StringVar()
        self.peer = tk.StringVar()
        self.exit = False
        self.peers = ["Select"]
        self.peer_lock = threading.Lock()
        self.window.geometry(f"{self.w}x{self.h}")
        self.window.title(title)
        self.window.config(background="#151515")
        self.top()
        self.bottom()
        self.window.mainloop()
        self.exit = True
        exit()

    def send(self):
        msg = self.msg.get()
        if not msg:
            return
        addr = self.peer.get()
        self.final_msg(addr, msg)
        msg = [addr, msg]
        self.client.msg = msg

    def final_msg(self, addr, msg):
        self.client.lock_final.acquire()
        if addr not in self.client.final_msg:
            self.client.final_msg[addr] = {"recv": [], "sent": []}
        self.client.final_msg[addr]["sent"].append((time.time(), msg))
        self.client.lock_final.release()

    
    @property
    def Adresses(self):
        self.peer_lock.acquire()
        t = self.peers
        self.peer_lock.release()
        return t
    
    @Adresses.setter
    def Addresses(self, arr):
        self.peer_lock.acquire()
        self.peers = arr
        self.peer_lock.release()


    def update_ip(self):
        s = self.peers
        ip = self.ip
        while True:
            self.client.lock_addrs.acquire()
            self.Addresses = self.client.addrs
            self.client.lock_addrs.release()
            if self.exit:
                self.client.exit = True
                return
            t = self.Addresses
            if t==s:    continue
            menu = ip["menu"]
            menu.delete(0, "end")
            for string in t:
                menu.add_command(label=string, command=lambda value=string: self.peer.set(value))
            s = t
            
        
    def top(self):
        if self.w<700:
            w = 0.8*self.w
        else:
            w = self.w
        frame = tk.Frame(self.window, background="#151515", padx=10, pady=10)   #Frame
        frame.place(x = 0, y = 0, width=self.w, height=0.2*self.h)
        
        self.ip = tk.OptionMenu(frame, self.peer, *self.peers)                     ### Peer - Options
        self.ip.config(width=20)
        self.ip.grid(column=1, row=1, padx=10, pady=10)
        threading.Thread(target=self.update_ip, args=()).start()
        #connect = tk.Button(frame, text="Connect", command=self.update_ip, padx=1)
        #connect.grid(column=1, row=2)

        txt_label = tk.Label(frame, text="Text: ", background="#151515", foreground="#FFFFFF", font="Helvetica 15 bold")
        txt_label.grid(column=2, row=1, padx=(30, 10))                                               ### MSG
        txt_entry = tk.Entry(frame, textvariable=self.msg, width=int(round(w*0.06)), font="Helvetica 11")
        txt_entry.grid(column=3, row=1)
        txt_send = tk.Button(frame, text="Send", padx=5, command=self.send)
        txt_send.grid(column=4, row=1, padx=(20,0))


    def bottom(self):
        self.bottomFrame = tk.Frame(self.window, background="#151515")   #Frame
        self.bottomFrame.place(x = 0, y = 0.2*self.h, width=self.w, height=0.8*self.h)
        threading.Thread(target=self.bottomSet, args=()).start()

    
    def bottomSet(self):
        tk.Label(self.bottomFrame, text="Last Received", background="#151515", foreground="#FFFFFF", font="Helvetica 12 bold", width=int(self.w*0.05)).grid(column=1, row=0, pady=10, padx=10)
        tk.Label(self.bottomFrame, text="Last Sent", background="#151515", foreground="#FFFFFF", font="Helvetica 12 bold", width=int(self.w*0.05)).grid(row=0, column=2, pady=10, padx=10)
        a = None
        b = None
        while True:
            if self.exit == True:
                return
            time.sleep(1)
            if a:
                a.destroy()
            if b:
                b.destroy()
            addr = self.peer.get()
            #self.client.lock_final.acquire()
            try:
                temp = self.client.final_msg[addr]
            except Exception as e:
            #    self.client.lock_final.release()
                print(e)
            #self.client.lock_final.release()
            i = 1
            try:
                t1 = temp["recv"][-1]
            except:
                t1 = [1, '']
            try:
                t2 = temp["sent"][-1]
            except:
                t2 = [1, '']
            
            a = tk.Label(self.bottomFrame, text=t1[-1], background="#151515", foreground="#FFFFFF", font="Helvetica 12 bold", width=int(self.w*0.05)).grid(column=1, row=i, pady=10, padx=10)
            b = tk.Label(self.bottomFrame, text=t2[-1], background="#151515", foreground="#FFFFFF", font="Helvetica 12 bold", width=int(self.w*0.05)).grid(row=i, column=2, pady=10, padx=10)

        

class Client_impl(Client):
    def __init__(self, ip="127.0.0.1", port=6969, selfIP=socket.gethostbyname(socket.gethostname())):
        super().__init__(ip, port, selfIP)
        self.final_msg = {}
        self.addrs = []
        self.lock_addrs = threading.Lock()
        self.lock_final = threading.Lock()
        self.refresh = True
    
    def addr(self, rmsg):
        rmsg = eval(rmsg)
        self.lock_addrs.acquire()
        self.addrs = rmsg["addr"]
        self.lock_addrs.release()
        del rmsg["addr"]
        addrs = list(rmsg.keys())
        for x in addrs:
            self.lock_final.acquire()
            if x in self.final_msg:
                self.final_msg[x]["recv"].append((time.time(), rmsg[x]))
            else:
                self.final_msg[x] = {"recv": [(time.time(), rmsg[x])], "sent": []}
            self.lock_final.release()




if __name__=="__main__":
    t = Main()