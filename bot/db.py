from pymongo import MongoClient

# MongoDB URL (Replace with your connection string)
MONGO_URL = "mongodb+srv://username:password@cluster0.mongodb.net/?retryWrites=true&w=majority"

# Create a client
client = MongoClient(MONGO_URL)

# Choose database name
db = client["hinatax_support_bot"]

# Create collections
users_collection = db["users"]   # Users collection (id, username, etc)
broadcast_collection = db["broadcasts"]  # Optional for broadcast history (if you want)