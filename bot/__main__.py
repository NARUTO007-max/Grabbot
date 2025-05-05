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
        caption=f"**Welcome {message.from_user.first_name} to Battle Arena!**\nChoose your destiny and fight legendary enemies!",
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
            [InlineKeyboardButton("Naruto", callback_data="verse_naruto")],
            [InlineKeyboardButton("One Piece", callback_data="verse_onepiece")],
            [InlineKeyboardButton("Bleach", callback_data="verse_bleach")]
        ]
    )

    # Delete previous message to avoid duplication
    await callback_query.message.delete()

    # Send only one message with photo and keyboard
    await callback_query.message.reply_photo(
        photo="https://files.catbox.moe/b0co3e.jpg",  # verse selection image
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

    # Character data (character name and stats)
    characters = {
        "naruto": {
            "name": "Naruto Uzumaki", 
            "power": 120, "defense": 90, "focus": 85, "agility": 95, "battle_iq": 75, "ki_manifestation": 80,
            "moves": "Rasengan, Shadow Clone Jutsu"
        },
        "sasuke": {
            "name": "Sasuke Uchiha", 
            "power": 130, "defense": 85, "focus": 90, "agility": 90, "battle_iq": 95, "ki_manifestation": 85,
            "moves": "Chidori, Fireball Jutsu"
        },
        "kakashi": {
            "name": "Kakashi Hatake", 
            "power": 115, "defense": 100, "focus": 95, "agility": 80, "battle_iq": 100, "ki_manifestation": 90,
            "moves": "Kamui, Lightning Blade"
        },
        "luffy": {
            "name": "Monkey D. Luffy", 
            "power": 140, "defense": 85, "focus": 80, "agility": 110, "battle_iq": 70, "ki_manifestation": 75,
            "moves": "Gomu Gomu no Pistol, Gear Second"
        },
        "zoro": {
            "name": "Roronoa Zoro", 
            "power": 130, "defense": 95, "focus": 85, "agility": 85, "battle_iq": 80, "ki_manifestation": 90,
            "moves": "Santoryu, Asura"
        },
        "sanji": {
            "name": "Vinsmoke Sanji", 
            "power": 125, "defense": 90, "focus": 95, "agility": 100, "battle_iq": 85, "ki_manifestation": 80,
            "moves": "Diable Jambe, Sky Walk"
        },
        "ichigo": {
            "name": "Ichigo Kurosaki", 
            "power": 135, "defense": 80, "focus": 95, "agility": 90, "battle_iq": 85, "ki_manifestation": 85,
            "moves": "Getsuga Tensho, Bankai"
        },
        "rukia": {
            "name": "Rukia Kuchiki", 
            "power": 110, "defense": 85, "focus": 90, "agility": 80, "battle_iq": 95, "ki_manifestation": 80,
            "moves": "Sode no Shirayuki"
        },
        "byakuya": {
            "name": "Byakuya Kuchiki", 
            "power": 125, "defense": 100, "focus": 95, "agility": 85, "battle_iq": 100, "ki_manifestation": 95,
            "moves": "Senbonzakura Kageyoshi"
        }
    }

    # Get character data
    char_data = characters.get(char)

    if char_data:
        char_name = char_data["name"]
        power = char_data["power"]
        defense = char_data["defense"]
        focus = char_data["focus"]
        agility = char_data["agility"]
        battle_iq = char_data["battle_iq"]
        ki_manifestation = char_data["ki_manifestation"]
        moves = char_data["moves"]

        stats = f"""**Congratulations! 🎉 You have unlocked {char_name}! 🌟**

**Stats:**
⚔️ Power: {power}
🛡️ Defense: {defense}
🎯 Focus: {focus}
⚡️ Agility: {agility}
🧠 Battle IQ: {battle_iq}
🔮 Ki Manifestation: {ki_manifestation}

**Moves Unlocked:**
{moves}
"""

        # Send stats message with character's image
        await callback_query.message.delete()
        await callback_query.message.reply_photo(
            photo=char_image,  # Use character's specific image URL here
            caption=stats
        )
        await callback_query.answer("Warrior Selected!")
    else:
        await callback_query.answer("Invalid character selected!")

print("Bot is running...")
bot.run()