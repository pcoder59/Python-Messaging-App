import socket
import threading
import tkinter as tk

def returnname():
    def receiving():
        receiving = True
        while receiving:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                TEXTAREA.insert("end", msg)
                TEXTAREA.see("end")
            
    def send(msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
            
    def sendmessage():
        mess = MESSAGEFIELD.get()
        MESSAGEFIELD.delete(0, "end")
        send(mess)
        
    def quitmessage():
        send(DISCONNECT_MESSAGE)
        exit()
    
    name = FIELD.get()
    FIELD.pack_forget()
    BUTTON.pack_forget()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    message = name.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    thread = threading.Thread(target=receiving)
    thread.daemon = True
    thread.start()
    MESSAGEFIELD = tk.Entry(TOP)
    SENDBUTTON = tk.Button(TOP, text="Send", command=sendmessage)
    QUITBUTTON = tk.Button(TOP, text="Quit", command=quitmessage)
    TEXTAREA = tk.Listbox(TOP)
    SCROLLBAR = tk.Scrollbar(TOP)
    MESSAGEFIELD.pack()
    SENDBUTTON.pack()
    QUITBUTTON.pack()
    TEXTAREA.pack(side="left", expand=True, fill="both")
    SCROLLBAR.pack(side="right", fill="both")
    SCROLLBAR.config(command=TEXTAREA.yview)

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = "172.105.62.42"
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

back = tk.Tk()
back.title("Python Messager")
TOP = tk.Frame(back, width=750, height=750)
TOP.pack_propagate(0)
TOP.pack()
FIELD = tk.Entry(TOP)
FIELD.insert(0, "Enter Name Here")
BUTTON = tk.Button(TOP, text="Send", command=returnname)
FIELD.pack(expand=True)
BUTTON.pack(expand=True)
TOP.mainloop()