import sqlite3

# DB connection
conn = sqlite3.connect("waifu.db", check_same_thread=False)
cur = conn.cursor()

# Rarity emoji mapping
RARITY_EMOJIS = {
    "Common": "⚪️",
    "Rare": "🔵",
    "Epic": "🟣",
    "Legendary": "🟡",
    "Special Edition": "💮"
}

# DB initialization
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
            hint TEXT,
            rarity TEXT CHECK(rarity IN ('Common', 'Rare', 'Epic', 'Legendary', 'Special Edition'))
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

# Add user to DB
def add_user(user_id, username, full_name):
    cur.execute("INSERT OR IGNORE INTO users (user_id, username, full_name) VALUES (?, ?, ?)",
                (user_id, username, full_name))
    conn.commit()

# Get waifus owned by user
def get_user_waifus(user_id):
    cur.execute("""
        SELECT w.name, w.anime, w.image, w.rarity
        FROM user_waifus uw
        JOIN waifus w ON uw.waifu_id = w.id
        WHERE uw.user_id = ?
        ORDER BY uw.timestamp DESC
    """, (user_id,))
    return cur.fetchall()

# Add waifu to DB
def add_waifu(name, anime, image, hint, rarity):
    cur.execute("""
        INSERT INTO waifus (name, anime, image, hint, rarity)
        VALUES (?, ?, ?, ?, ?)
    """, (name, anime, image, hint, rarity))
    conn.commit()

# Assign waifu to user
def assign_waifu_to_user(user_id, waifu_id, timestamp):
    cur.execute("INSERT INTO user_waifus (user_id, waifu_id, timestamp) VALUES (?, ?, ?)",
                (user_id, waifu_id, timestamp))
    conn.commit()