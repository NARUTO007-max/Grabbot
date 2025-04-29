from pymongo import MongoClient

# MongoDB URL (Replace with your connection string)
MONGO_URL = "mongodb+srv://sufyan532011:2010@dbz.28ftn.mongodb.net/?retryWrites=true&w=majority&appName=DBZ"

# Create a client
client = MongoClient(MONGO_URL)

# Choose database name
db = client["hinatax_support_bot"]

# Create collections
users_collection = db["users"]   # Users collection (id, username, etc)
broadcast_collection = db["broadcasts"]  # Optional for broadcast history (if you want)

from datetime import datetime

async def get_top_daily_users():
    today = datetime.today()

    pipeline = [
        {
            "$match": {
                "last_message_date": {"$gte": datetime(today.year, today.month, today.day)}
            }
        },
        {
            "$project": {
                "username": 1,
                "daily_count": 1
            }
        },
        {
            "$sort": {"daily_count": -1}
        },
        {
            "$limit": 10
        }
    ]

    top_users_cursor = users_collection.aggregate(pipeline)
    top_users = []
    total_messages = 0

    async for user in top_users_cursor:
        username = user.get("username", "Unknown")
        count = user.get("daily_count", 0)
        top_users.append((username, count))
        total_messages += count

    return top_users, total_messages