import sqlite3

# Database initialize
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT
)
""")
conn.commit()

# Function to check if user exists
def user_exists(user_id):
    cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None

# Function to add a new user
def add_user(user_id, name):
    if not user_exists(user_id):
        cursor.execute("INSERT INTO users (user_id, name) VALUES (?, ?)", (user_id, name))
        conn.commit()