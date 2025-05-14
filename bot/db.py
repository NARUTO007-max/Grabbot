# db.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["anime_multiverse"]
users = db["users"]

def get_or_create_user(user_id, username):
    user = users.find_one({"user_id": user_id})
    if not user:
        user = {
            "user_id": user_id,
            "username": username,
            "selected_character": None,
            "level": 1,
            "gold": 0,
            "diamonds": 0,
            "current_universe": None,
        }
        users.insert_one(user)
    return user

def set_character(user_id, character_name):
    users.update_one(
        {"user_id": user_id},
        {"$set": {"selected_character": character_name}}
    )