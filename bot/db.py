import sqlite3

# Initialize database and tables
def init_db():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()

    # Create table for storing waifu details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS waifus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_url TEXT,
            anime_name TEXT,
            character_name TEXT,
            rarity INTEGER
        )
    ''')

    # Create table for storing group info
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER PRIMARY KEY
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Add waifu to database
def add_waifu(image_url, anime_name, character_name, rarity):
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO waifus (image_url, anime_name, character_name, rarity)
        VALUES (?, ?, ?, ?)
    ''', (image_url, anime_name, character_name, rarity))

    conn.commit()
    conn.close()

# Get all waifus
def get_all_waifus():
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM waifus')
    waifus = cursor.fetchall()

    conn.close()
    return waifus

# Get random waifu from DB
def get_random_waifu():
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM waifus ORDER BY RANDOM() LIMIT 1')
    waifu = cursor.fetchone()

    conn.close()
    return waifu

# Add group to the database
def add_group(group_id):
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR IGNORE INTO groups (group_id)
        VALUES (?)
    ''', (group_id,))

    conn.commit()
    conn.close()

# Get all groups
def get_all_group_ids():
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()

    cursor.execute('SELECT group_id FROM groups')
    groups = cursor.fetchall()

    conn.close()
    return [group[0] for group in groups]