import sqlite3
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Config
api_id = 25698862
api_hash = "7d7739b44f5f8c825d48cc6787889dbc"
bot_token = "8068521367:AAFHqYZnf7DnsSWFpN8bk_ffJ5Qe3giRbNw"

bot = Client("battle_game_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Initialize DB
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT)")
conn.commit()

@bot.on_message(filters.command("start") & filters.private)
async def start_game(client, message):
    user_id = message.from_user.id
    name = message.from_user.first_name

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if user:
        await message.reply_text("**You already started the bot!**")
        return

    # New user: add to DB
    cursor.execute("INSERT INTO users (user_id, name) VALUES (?, ?)", (user_id, name))
    conn.commit()

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("▶️ Start Game", callback_data="start_game")]]
    )

    await message.reply_photo(
        photo="https://files.catbox.moe/461mqe.jpg",
        caption=f"**Welcome {name} to Battle Arena!**\nChoose your destiny and fight legendary enemies!",
        reply_markup=keyboard
    )

@bot.on_callback_query(filters.regex("start_game"))
async def continue_game(client, callback_query):
    await callback_query.message.edit_caption(
        "**Your journey begins now...**\nAre you ready to train?",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Continue", callback_data="continue_journey")]]
        )
    )
    await callback_query.answer()

@bot.on_callback_query(filters.regex("continue_journey"))
async def choose_verse(client, callback_query):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Naruto", callback_query="verse_naruto")],
            [InlineKeyboardButton("One Piece", callback_query="verse_onepiece")],
            [InlineKeyboardButton("Bleach", callback_query="verse_bleach")]
        ]
    )
    await callback_query.message.delete()
    await callback_query.message.reply_photo(
        photo="https://files.catbox.moe/b0co3e.jpg",  # tu yahan apni anime verse image daal
        caption="**Choose your Anime Verse for training:**",
        reply_markup=keyboard
    )
    await callback_query.answer()

@bot.on_callback_query(filters.regex("verse_(naruto|onepiece|bleach)"))
async def choose_character(client, callback_query):
    verse = callback_query.data.split("_")[1]

    # Character data
    characters = {
        "naruto": [
            ("Naruto Uzumaki", "char_naruto"),
            ("Sasuke Uchiha", "char_sasuke"),
            ("Kakashi Hatake", "char_kakashi")
        ],
        "onepiece": [
            ("Luffy", "char_luffy"),
            ("Zoro", "char_zoro"),
            ("Sanji", "char_sanji")
        ],
        "bleach": [
            ("Ichigo", "char_ichigo"),
            ("Rukia", "char_rukia"),
            ("Byakuya", "char_byakuya")
        ]
    }

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(name, callback_data=data)] for name, data in characters[verse]]
    )

    await callback_query.message.delete()
    await callback_query.message.reply_photo(
        photo=f"https://files.catbox.moe/b0co3e.jpg",  # yahan per tu har verse ke characters ki photo laga
        caption=f"**{verse.capitalize()} Verse Selected!**\nNow choose your warrior:",
        reply_markup=keyboard
    )
    await callback_query.answer()

@bot.on_callback_query(filters.regex("char_"))
async def final_character(client, callback_query):
    char = callback_query.data.split("_")[1]

    # Dummy image URLs for characters
    char_images = {
        "naruto": "https://files.catbox.moe/lk4n3b.jpg",
        "sasuke": "https://files.catbox.moe/di4o7h.jpg",
        "kakashi": "https://files.catbox.moe/mwife4.jpg",
        "luffy": "https://files.catbox.moe/v76o15.jpg",
        "zoro": "https://files.catbox.moe/ik5x9k.jpg",
        "sanji": "https://files.catbox.moe/xye0wp.jpg",
        "ichigo": "https://files.catbox.moe/8bcu89.jpg",
        "rukia": "https://files.catbox.moe/v1udxj.jpg",
        "byakuya": "https://files.catbox.moe/ilgdpy.jpg",
    }

    stats = f"**{char.capitalize()} Selected!**\n\n**Level**: 1\n**Power**: 120\n**Defense**: 90\n**Speed**: 100\n\nLet the battles begin!"

    await callback_query.message.delete()
    await callback_query.message.reply_photo(
        photo=char_images.get(char, "https://your-image-url.com/default.jpg"),
        caption=stats
    )
    await callback_query.answer("Warrior Selected!")

print("Bot is running...")
bot.run()