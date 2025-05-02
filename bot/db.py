import sqlite3
from datetime import datetime

# DB connection
conn = sqlite3.connect("waifu.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
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
    with conn:
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
                quantity INTEGER DEFAULT 1,
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                FOREIGN KEY(waifu_id) REFERENCES waifus(id),
                PRIMARY KEY(user_id, waifu_id)
            )
        """)

# Add user to DB
def add_user(user_id, username, full_name):
    with conn:
        cur.execute("""
            INSERT OR IGNORE INTO users (user_id, username, full_name)
            VALUES (?, ?, ?)
        """, (user_id, username, full_name))

# Get waifus owned by user
def get_user_waifus(user_id):
    cur.execute("""
        SELECT w.id, w.name, w.anime, w.image, w.rarity, uw.quantity
        FROM user_waifus uw
        JOIN waifus w ON uw.waifu_id = w.id
        WHERE uw.user_id = ?
        ORDER BY uw.timestamp DESC
    """, (user_id,))
    return [dict(row) for row in cur.fetchall()]

# Add waifu to DB
def add_waifu(name, anime, image, hint, rarity):
    with conn:
        cur.execute("""
            INSERT INTO waifus (name, anime, image, hint, rarity)
            VALUES (?, ?, ?, ?, ?)
        """, (name, anime, image, hint, rarity))

# Assign waifu to user
def assign_waifu_to_user(user_id, waifu_id, timestamp=None):
    if not timestamp:
        timestamp = datetime.utcnow().isoformat()
    with conn:
        cur.execute("""
            INSERT OR IGNORE INTO user_waifus (user_id, waifu_id, timestamp, quantity)
            VALUES (?, ?, ?, 1)
        """, (user_id, waifu_id, timestamp))
        cur.execute("""
            UPDATE user_waifus
            SET quantity = quantity + 1
            WHERE user_id = ? AND waifu_id = ?
        """, (user_id, waifu_id))

# Get waifu by user ID and waifu ID
def get_waifu_by_user(user_id, waifu_id):
    cur.execute("""
        SELECT *
        FROM user_waifus
        WHERE user_id = ? AND waifu_id = ?
    """, (user_id, waifu_id))
    return cur.fetchone()

# Update waifu quantity
def update_waifu_quantity(user_id, waifu_id, quantity):
    with conn:
        cur.execute("""
            UPDATE user_waifus
            SET quantity = ?
            WHERE user_id = ? AND waifu_id = ?
        """, (quantity, user_id, waifu_id))

# Add or update waifu for user
def add_or_update_waifu(user_id, waifu_id, timestamp=None):
    if not timestamp:
        timestamp = datetime.utcnow().isoformat()
    existing = get_waifu_by_user(user_id, waifu_id)
    if existing:
        update_waifu_quantity(user_id, waifu_id, existing['quantity'] + 1)
    else:
        assign_waifu_to_user(user_id, waifu_id, timestamp)