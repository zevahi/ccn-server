CREATE TABLE IF NOT EXISTS
messages_t (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    content TEXT,
    time_sent INTEGER,
    )