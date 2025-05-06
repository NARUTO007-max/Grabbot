import os
from motor.motor_asyncio import AsyncIOMotorClient

# **MongoDB Connection**
MONGO_URI = "mongodb+srv://sufyan532011:5042@auctionbot.5ms20.mongodb.net/?retryWrites=true&w=majority&appName=AuctionBot"

if not MONGO_URI or "null" in MONGO_URI:
    raise ValueError("❌ MONGO_URI is missing or incorrect! Check your .env file.")

# **Connect to MongoDB**
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["AUC_BOT"]  # Replace with your DB name

# ✅ **Define Collections**
users_collection = db["users"]
admins_collection = db["admins"]
pending_submissions = db["pending_submissions"]
cooldowns_collection = db["cooldowns"]
submissions_collection = db["submissions"]
approved_items_collection = db["approved_items"]
bids_collection = db["bids"]

# ✅ **Save Submission to DB**
async def save_submission_to_db(user_id, data):
    """Save submission details to MongoDB."""
    await submissions_collection.update_one({"user_id": user_id}, {"$set": data}, upsert=True)

# ✅ **Retrieve Submission from DB**
async def get_submission_from_db(user_id):
    """Retrieve submission details from MongoDB."""
    return await submissions_collection.find_one({"user_id": user_id})

# ✅ **User Functions**
async def get_user(user_id):
    """Fetch user details from the database."""
    return await users_collection.find_one({"user_id": user_id})

async def add_user(user_id):
    """Add a new user to the database."""
    if not await get_user(user_id):
        await users_collection.insert_one({"user_id": user_id, "submissions": 0, "approved": 0, "rejected": 0})

async def update_user_stats(user_id, status):
    """Update user submission stats."""
    await add_user(user_id)  # Ensure user exists
    field_update = {
        "submitted": {"submissions": 1},
        "approved": {"approved": 1},
        "rejected": {"rejected": 1},
    }.get(status, {})

    if field_update:
        await users_collection.update_one({"user_id": user_id}, {"$inc": field_update})

# ✅ **Admin Functions**
async def is_admin(user_id):
    """Check if a user is an admin."""
    return await admins_collection.find_one({"user_id": user_id}) is not None

async def add_admin(user_id):
    """Add a user as an admin."""
    if not await is_admin(user_id):
        await admins_collection.insert_one({"user_id": user_id})

async def remove_admin(user_id):
    """Remove admin privileges from a user."""
    await admins_collection.delete_one({"user_id": user_id})

# ✅ **Cooldown Functions**
async def set_cooldown(user_id, timestamp):
    """Set cooldown for a user."""
    await cooldowns_collection.update_one({"user_id": user_id}, {"$set": {"timestamp": timestamp}}, upsert=True)

async def get_cooldown(user_id):
    """Retrieve cooldown timestamp for a user."""
    cooldown = await cooldowns_collection.find_one({"user_id": user_id})
    return cooldown["timestamp"] if cooldown else None

# ✅ **Submissions & Bidding**
async def add_submission(user_id, name, base_price, auction_link):
    """Add a new submission to the database."""
    await submissions_collection.insert_one({"user_id": user_id, "name": name, "base_price": base_price, "auction_link": auction_link})

async def place_bid(auction_id, user_id, bid_amount):
    """Update the highest bid for an auction."""
    await bids_collection.update_one({"auction_id": auction_id}, {"$set": {"highest_bid": bid_amount, "bidder_id": user_id}}, upsert=True)