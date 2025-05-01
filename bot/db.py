import sqlite3

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            chat_type TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(chat_id, chat_type="private"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (chat_id, chat_type) VALUES (?, ?)", (chat_id, chat_type))
    conn.commit()
    conn.close()

def get_all_chats():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT chat_id, chat_type FROM users")
    chats = c.fetchall()
    conn.close()
    return chats