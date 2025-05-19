from pymongo import MongoClient
import os

MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://sufyan532011:2010@dbz.28ftn.mongodb.net/?retryWrites=true&w=majority&appName=DBZ"
)
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

def set_favorite_waifu(user_id, waifu_id):
    waifu_col.update_one(
        {"user_id": user_id},
        {"$set": {"favorite_waifu_id": waifu_id}},
        upsert=True
    )

def get_user_waifus(user_id):
    return waifu_col.find_one({"user_id": user_id})

def remove_favorite_waifu(user_id):
    waifu_col.update_one(
        {"user_id": user_id},
        {"$unset": {"favorite_waifu_id": ""}}
    )