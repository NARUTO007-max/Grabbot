from pymongo import MongoClient
import os
from random import randint

MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://sufyan532011:2010@dbz.28ftn.mongodb.net/?retryWrites=true&w=majority&appName=DBZ"
)
client = MongoClient(MONGO_URI)

db = client["waifu_bot"]

waifu_col = db["waifus"]
upload_col = db["upload_waifus"]
config_col = db["bot_config"]  # For drop time and config
group_col = db["groups"]       # For storing group IDs

# --- User Functions ---

def add_waifu_to_user(user_id, username, waifu_data):
    waifu_col.update_one(
        {"user_id": user_id},
        {
            "$set": {"username": username},
            "$push": {"waifus": waifu_data}
        },
        upsert=True
    )

def get_user_waifus(user_id):
    return waifu_col.find_one({"user_id": user_id})

def set_favorite_waifu(user_id, waifu_id):
    waifu_col.update_one(
        {"user_id": user_id},
        {"$set": {"favorite_waifu_id": waifu_id}},
        upsert=True
    )

def remove_favorite_waifu(user_id):
    waifu_col.update_one(
        {"user_id": user_id},
        {"$unset": {"favorite_waifu_id": ""}}
    )

# --- Waifu Upload & Drop Functions ---

def upload_waifu(data):
    return upload_col.insert_one(data)

def get_random_waifu():
    count = upload_col.count_documents({})
    if count == 0:
        return None
    skip = randint(0, count - 1)
    return upload_col.find().skip(skip).limit(1)[0]

# --- Drop Timer Configuration ---

def set_drop_time(seconds: int):
    config_col.update_one({"_id": "drop_config"}, {"$set": {"drop_time": seconds}}, upsert=True)

def get_drop_time():
    config = config_col.find_one({"_id": "drop_config"})
    return config.get("drop_time", 60) if config else 60

# --- Group Management for /fdrop ---

def add_group(chat_id):
    group_col.update_one({"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)

def get_all_groups():
    return [group["chat_id"] for group in group_col.find()]