import sqlite3
from pathlib import Path


class databaseManager:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.sql_dir = Path(__file__).parent / "sql"
        self.create_users_t = (
            Path(self.sql_dir / "create_users_t.sql").read_text().replace("\n", "")
        )
        self.create_messages_t = (
            Path(self.sql_dir / "create_messages_t").read_text().replace("\n", "")
        )
        self.insert_message_sql = (
            Path(self.sql_dir / "insert_message").read_text().replace("\n", "")
        )

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute(self.create_users_t)
        cursor.execute(self.create_messages_t)
        cursor.close()

    def insert_message(self, message, sender_id, time_sent):
        cursor = self.conn.cursor()
        cursor.execute(
            self.insert_message_sql,
            (
                sender_id,
                message["content"],
                message["receiver_id"],
                time_sent,
            ),
        )
        cursor.close()
