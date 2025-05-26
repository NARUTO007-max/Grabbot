import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("QTBot.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
cur.execute("CREATE TABLE IF NOT EXISTS premium (user_id INTEGER PRIMARY KEY, premium_until TEXT)")
conn.commit()

def add_user(user_id):
    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

def add_premium(user_id):
    expire_date = datetime.utcnow() + timedelta(days=30)
    cur.execute("INSERT OR REPLACE INTO premium (user_id, premium_until) VALUES (?, ?)",
                (user_id, expire_date.isoformat()))
    conn.commit()

def is_premium(user_id):
    cur.execute("SELECT premium_until FROM premium WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    if result:
        expire_time = datetime.fromisoformat(result[0])
        if datetime.utcnow() < expire_time:
            return True
        else:
            remove_premium(user_id)  # Auto remove if expired
    return False

def remove_premium(user_id):
    cur.execute("DELETE FROM premium WHERE user_id = ?", (user_id,))
    conn.commit()