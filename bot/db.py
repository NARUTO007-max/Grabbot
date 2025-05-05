import sqlite3

conn = sqlite3.connect("bot_data.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    is_connected INTEGER DEFAULT 0
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS channels (
    user_id INTEGER,
    channel_id INTEGER,
    channel_name TEXT,
    channel_username TEXT
)""")

conn.commit()

def add_user(user_id):
    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

def set_connected(user_id, status: int):
    cur.execute("UPDATE users SET is_connected=? WHERE user_id=?", (status, user_id))
    conn.commit()

def is_user_connected(user_id):
    cur.execute("SELECT is_connected FROM users WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] == 1 if result else False

def add_channel(user_id, channel_id, name, username):
    cur.execute("INSERT INTO channels (user_id, channel_id, channel_name, channel_username) VALUES (?, ?, ?, ?)",
                (user_id, channel_id, name, username))
    conn.commit()

def get_user_channels(user_id):
    cur.execute("SELECT channel_name, channel_username FROM channels WHERE user_id=?", (user_id,))
    return cur.fetchall()