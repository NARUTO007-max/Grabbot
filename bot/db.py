import sqlite3
import json

conn = sqlite3.connect("quiz.db", check_same_thread=False)
cur = conn.cursor()

def setup_db():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            options TEXT,
            correct_option INTEGER
        )
    """)
    conn.commit()

def add_quiz(question, options, correct_index):
    cur.execute("INSERT INTO quiz (question, options, correct_option) VALUES (?, ?, ?)",
                (question, json.dumps(options), correct_index))
    conn.commit()

def get_random_quiz():
    cur.execute("SELECT * FROM quiz ORDER BY RANDOM() LIMIT 1")
    row = cur.fetchone()
    if row:
        return {
            "id": row[0],
            "question": row[1],
            "options": json.loads(row[2]),
            "correct_option": row[3]
        }