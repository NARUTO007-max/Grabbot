from pymongo import MongoClient

# MongoDB URL (Replace with your connection string)
MONGO_URL = "mongodb+srv://Naruto:Naruto7775549@cluster1.ge8jrgm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"

# Create a client
client = MongoClient(MONGO_URL)

# Choose database name
db = client["hinatax_support_bot"]

# Create collections
users_collection = db["users"]   # Users collection (id, username, etc)
broadcast_collection = db["broadcasts"]  # Optional for broadcast history (if you want)