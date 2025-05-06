import os

API_ID = int(os.getenv("API_ID", 25698862))
API_HASH = os.getenv("API_HASH", "7d7739b44f5f8c825d48cc6787889dbc")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7596130411:AAFf-i7Nq_Yem6Dr-l0SKrUbrxq-nGoldUI")

APPROVAL_GROUP_ID = int(os.getenv("APPROVAL_GROUP_ID", -1002149313669))
AUCTION_GROUP_LINK = os.getenv("AUCTION_GROUP_LINK", "https://t.me/Trainers_union")
AUCTION_CHANNEL_ID = int(os.getenv("AUCTION_CHANNLE_ID", -1002343088713))  # Typo fix: AUCTION_CHANNLE_ID → AUCTION_CHANNEL_ID
AUCTION_CHANNEL_LINK = os.getenv("AUCTION_CHANNEL_LINK", "https://t.me/God_Auction")

OWNER_IDS = list(map(int, os.getenv("OWNER_IDS", "7019600964").split(",")))  # Fixed default to string
COOLDOWN_TIME = int(os.getenv("COOLDOWN_TIME", 60))