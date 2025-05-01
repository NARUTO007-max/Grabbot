import sqlite3

conn = sqlite3.connect("waifu.db", check_same_thread=False)
cur = conn.cursor()

def init_db():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            total_waifus INTEGER DEFAULT 0,
            gifted INTEGER DEFAULT 0,
            received INTEGER DEFAULT 0
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS waifus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            anime TEXT,
            image TEXT,
            hint TEXT
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_waifus (
            user_id INTEGER,
            waifu_id INTEGER,
            timestamp TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(waifu_id) REFERENCES waifus(id)
        )
    """)
    
    conn.commit()

def add_user(user_id, username, full_name):
    cur.execute("INSERT OR IGNORE INTO users (user_id, username, full_name) VALUES (?, ?, ?)", (user_id, username, full_name))
    conn.commit()

def get_user_waifus(user_id):
    cur.execute("""
        SELECT w.name, w.anime, w.image
        FROM user_waifus uw
        JOIN waifus w ON uw.waifu_id = w.id
        WHERE uw.user_id = ?
        ORDER BY uw.timestamp DESC
    """, (user_id,))
    return cur.fetchall()