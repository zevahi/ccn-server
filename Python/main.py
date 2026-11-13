from db_manager import databaseManager
from server import serverManager


def main():
    host = "0.0.0.0"
    port = 24680

    db_man = databaseManager("data/chats.db")
    db_man.create_tables()

    server = serverManager(host, port)
    while True:
        server.accept_client()


if __name__ == "__main__":
    main()
