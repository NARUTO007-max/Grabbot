from pyrogram import Client, filters 
import config 
import sys 
import os  
import logging

# Basic logging configuration
logging.basicConfig(
    format="[KURO-ZONE] ==> %(asctime)s - %(levelname)s - %(message)s", 
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

bot = Client("CHANDU", 
             api_id=config.API_ID,
             api_hash=config.API_HASH, 
             bot_token=config.BOT_TOKEN, 
             plugins=dict(root="AB"))