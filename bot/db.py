import sqlite3

conn = sqlite3.connect("qtbot.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
c.execute("CREATE TABLE IF NOT EXISTS premium (user_id INTEGER PRIMARY KEY)")

def add_user(user_id: int):
    c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

def add_premium(user_id: int):
    c.execute("INSERT OR IGNORE INTO premium (user_id) VALUES (?)", (user_id,))
    conn.commit()

def is_premium(user_id: int) -> bool:
    return c.execute("SELECT 1 FROM premium WHERE user_id=?", (user_id,)).fetchone() is not None