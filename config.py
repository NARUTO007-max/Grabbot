import os

API_ID = int(os.environ.get("API_ID", 25698862))
API_HASH = os.environ.get("API_HASH", "7d7739b44f5f8c825d48cc6787889dbc")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7900777297:AAHOO4aS-Bx5WRScOVglWRWsa8m5n5vdwvQ")

# Owner ID(s)
OWNER_ID = int(os.environ.get("OWNER_ID", 7576729648))  # Replace with your actual Telegram user ID
OWNER_IDS = [OWNER_ID]  # For multiple owners, extend this list

# Optional MongoDB (in case used here too)
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://sufyan532011:2010@dbz.28ftn.mongodb.net/?retryWrites=true&w=majority&appName=DBZ"
)