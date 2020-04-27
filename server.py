import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
clients_lock = threading.Lock()

def handle_client(conn, addr):
    name = conn.recv(HEADER).decode(FORMAT)
    if name:
        name = int(name)
        msg_name = conn.recv(name).decode(FORMAT)
    print(f"[NEW CONNECTION] {msg_name} connected.")
    connection_message = f"{msg_name} connected."
    with clients_lock:
        for c in range(len(clients)):
            try:
                if clients[c] != conn:
                    try:
                        message = connection_message.encode(FORMAT)
                        msg_length = len(message)
                        send_length = str(msg_length).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        clients[c].sendall(send_length)
                        clients[c].sendall(message)
                    except:
                        clients.remove(clients[c])
                        
            except:
                continue
    
    with clients_lock:
        clients.append(conn)
    
    connected = True
    try:
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg1 = conn.recv(msg_length).decode(FORMAT)
                msg = f"{msg_name}: {msg1}"
                if msg1 == DISCONNECT_MESSAGE:
                    connected = False
                print(f"{msg}")
                with clients_lock:
                    for c in range(len(clients)):
                        try:
                            if clients[c] != conn:
                                try:
                                    message = msg.encode(FORMAT)
                                    msg_length = len(message)
                                    send_length = str(msg_length).encode(FORMAT)
                                    send_length += b' ' * (HEADER - len(send_length))
                                    clients[c].sendall(send_length)
                                    clients[c].sendall(message)
                                except:
                                    clients.remove(clients[c])
                        except:
                            continue
                msg = f"You: {msg1}"
                message = msg.encode(FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                conn.send(send_length)
                conn.send(message)
                
    finally:
        with clients_lock:
            clients.remove(conn)
            conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {len(clients) + 1}")

print("[STARTING] server is starting...")
start()