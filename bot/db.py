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

def preload_quizzes():
    questions = [
        ("Who is the main protagonist of Naruto?", ["Sasuke", "Naruto", "Sakura", "Kakashi"], 1),
        ("Which anime features a notebook that kills?", ["Bleach", "One Piece", "Death Note", "Naruto"], 2),
        ("Luffy wants to become the?", ["Wizard King", "Pirate King", "Hokage", "Shinigami"], 1),
        ("Goku belongs to which race?", ["Saiyan", "Namekian", "Human", "God"], 0),
        ("What does Sharingan belong to?", ["Senju", "Uchiha", "Hyuga", "Kaguya"], 1),
        ("Who killed Ace in One Piece?", ["Akainu", "Blackbeard", "Kaido", "Doflamingo"], 0),
        ("Who is the captain of Squad 6 in Bleach?", ["Kenpachi", "Byakuya", "Ichigo", "Toshiro"], 1),
        ("Which anime has alchemy as its main theme?", ["One Piece", "Fullmetal Alchemist", "Bleach", "Fairy Tail"], 1),
        ("In Demon Slayer, what is Nezuko?", ["Human", "Demon", "Vampire", "Ghost"], 1),
        ("Levi is a character from?", ["Naruto", "Bleach", "Attack on Titan", "Tokyo Ghoul"], 2),
    ]
    for q in questions:
        add_quiz(q[0], q[1], q[2])

# Run this only once
# preload_quizzes()