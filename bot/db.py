import sqlite3

# Initialize all required tables
def init_db():
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT
        )
    ''')

    # Create waifus table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS waifus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_url TEXT,
            anime_name TEXT,
            character_name TEXT,
            rarity INTEGER
        )
    ''')

    # Create user_waifus mapping table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_waifus (
            user_id INTEGER,
            waifu_id INTEGER,
            quantity INTEGER DEFAULT 1,
            PRIMARY KEY (user_id, waifu_id)
        )
    ''')

    # Create group table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER PRIMARY KEY
        )
    ''')

    conn.commit()
    conn.close()

# Add user to the users table
def add_user(user_id, username):
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username)
        VALUES (?, ?)
    ''', (user_id, username))
    conn.commit()
    conn.close()

# Add waifu to the waifus table
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

# Get a random waifu
def get_random_waifu():
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM waifus ORDER BY RANDOM() LIMIT 1')
    waifu = cursor.fetchone()
    conn.close()
    return waifu

# Get waifus linked to a user
def get_waifu_by_user(user_id):
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT w.* FROM waifus w
        INNER JOIN user_waifus uw ON w.id = uw.waifu_id
        WHERE uw.user_id = ?
    ''', (user_id,))
    waifus = cursor.fetchall()
    conn.close()
    return waifus

# Get user’s waifus (raw)
def get_user_waifus(user_id):
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM waifus WHERE id IN (
            SELECT waifu_id FROM user_waifus WHERE user_id = ?
        )
    ''', (user_id,))
    waifus = cursor.fetchall()
    conn.close()
    return waifus

# Update waifu quantity or insert if not present
def update_waifu_quantity(user_id, waifu_id, quantity):
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_waifus (user_id, waifu_id, quantity)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, waifu_id)
        DO UPDATE SET quantity = quantity + ?
    ''', (user_id, waifu_id, quantity, quantity))
    conn.commit()
    conn.close()

# Shortcut to add/update a waifu for user
def add_or_update_waifu(user_id, waifu_id):
    update_waifu_quantity(user_id, waifu_id, 1)

# Add group
def add_group(group_id):
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO groups (group_id)
        VALUES (?)
    ''', (group_id,))
    conn.commit()
    conn.close()

# Get all group IDs
def get_all_group_ids():
    conn = sqlite3.connect('waifu_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT group_id FROM groups')
    groups = cursor.fetchall()
    conn.close()
    return [group[0] for group in groups]