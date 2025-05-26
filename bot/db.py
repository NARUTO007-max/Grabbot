import sqlite3

conn = sqlite3.connect("qtbot.db", check_same_thread=False)
cursor = conn.cursor()

# Tables
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS premium (user_id INTEGER PRIMARY KEY)")
conn.commit()

# Add user to users table
def add_user(user_id: int):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

# Add user to premium table
def add_premium(user_id: int):
    cursor.execute("INSERT OR IGNORE INTO premium (user_id) VALUES (?)", (user_id,))
    conn.commit()

# Remove user from premium
def remove_premium(user_id: int):
    cursor.execute("DELETE FROM premium WHERE user_id = ?", (user_id,))
    conn.commit()

# Check if user is premium
def is_premium(user_id: int) -> bool:
    cursor.execute("SELECT 1 FROM premium WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None

# Get all premium users (optional)
def get_all_premium():
    cursor.execute("SELECT user_id FROM premium")
    return [row[0] for row in cursor.fetchall()]