import socket
import threading

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 24680
CHAT_SEPARATOR = "<SEP>"

# server_socket = socket.create_server(address=(localhost, port), family=socket.AF_INET)

def client_listener(client_socket):
    while(True):
        try:
            message = client_socket.recv(1024).decode()
        except Exception as e:
            print(f"Error: {e}")
            client_sockets.remove(client_socket)
        else:
            message = message.replace(CHAT_SEPARATOR, ": ")

        for sock in client_sockets:
            sock.sendall(message.encode())


client_sockets = set()

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen()
print(f"Listening on {SERVER_HOST}:{SERVER_PORT}")

while(True):
    client_socket, client_address = server.accept()
    client_sockets.add(client_socket)
    print(f"{client_address} Connected")

    c_thread = threading.Thread(target=client_listener, args=(client_socket))
    c_thread.daemon = True
    c_thread.start()
