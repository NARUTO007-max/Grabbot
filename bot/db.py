from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI", "your-mongodb-uri")
client = MongoClient(MONGO_URI)

db = client["waifu_bot"]
waifu_col = db["waifus"]

def add_waifu_to_user(user_id, username, waifu_data):
    waifu_col.update_one(
        {"user_id": user_id},
        {
            "$set": {"username": username},
            "$push": {"waifus": waifu_data}
        },
        upsert=True
    )