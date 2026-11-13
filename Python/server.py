import json
import socket
import threading
import time
from pathlib import Path

from db_manager import databaseManager


class serverManager:
    def __init__(self, host, port):
        # network stuff
        self.host = host
        self.port = port
        self.client_sockets = set()
        self.conn = socket.socket()

        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conn.bind((host, port))
        self.conn.listen()
        print(f"Listening on {self.host}:{self.port}")

        # database stuff
        self.db_path = Path(__file__).parent / "data" / "app.db"

    def accept_client(self):
        client_socket, client_address = self.conn.accept()
        self.client_sockets.add(client_socket)

        c_thread = threading.Thread(target=self.listener, args=(client_socket,))
        c_thread.daemon = True
        c_thread.start()

        print(f"{client_address} Connected")

    def listener(self, client_socket):
        db_man = databaseManager(self.db_path)
        metadata = {}
        handshake = True

        while True:
            try:
                message = client_socket.recv(1024).decode()
                time_sent = int(time.time() * 1000)
                if handshake:
                    metadata = self.parse_message(message)
                    handshake = False
                else:
                    db_man.insert_message(self.parse_message(message), sender_id, time_sent)

            except Exception as e:
                print(f"Error: {e}")
                self.client_sockets.remove(client_socket)
                break

            else:
                message = message.replace("<SEP>", ": ")

            for sock in self.client_sockets:
                sock.sendall(message.encode())

    def parse_hello(self, message):
        foo = json.load(message)
        return foo

    def parse_message(self, message):
        foo = json.load(message)
        return message
