from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api_id = 25698862
api_hash = "7d7739b44f5f8c825d48cc6787889dbc"
bot_token = "8068521367:AAFHqYZnf7DnsSWFpN8bk_ffJ5Qe3giRbNw"

bot = Client(
    "battle_game_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# Start command
@bot.on_message(filters.command("start") & filters.private)
async def start_game(client, message):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("▶️ Start Game", callback_data="start_game")]]
    )
    await message.reply_photo(
        photo="https://files.catbox.moe/461mqe.jpg",
        caption=f"**Welcome {message.from_user.first_name} to Battle Arena!**\nChoose your destiny and fight legendary enemies!",
        reply_markup=keyboard
    )

# Step 1: Start Game pressed
@bot.on_callback_query(filters.regex("start_game"))
async def continue_game(client, callback_query):
    await callback_query.message.edit_caption(
        "**Your journey begins now...**\nAre you ready to train?",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Continue", callback_data="continue_journey")]]
        )
    )
    await callback_query.answer()

# Step 2: Continue Journey
@bot.on_callback_query(filters.regex("continue_journey"))
async def choose_verse(client, callback_query):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Naruto", callback_data="verse_naruto")],
            [InlineKeyboardButton("One Piece", callback_data="verse_onepiece")],
            [InlineKeyboardButton("Bleach", callback_data="verse_bleach")]
        ]
    )
    await callback_query.message.edit_caption(
        "**Choose your Anime Verse for training:**",
        reply_markup=keyboard
    )
    await callback_query.answer()

# Step 3: Choose Verse → Show characters
@bot.on_callback_query(filters.regex("verse_(naruto|onepiece|bleach)"))
async def choose_character(client, callback_query):
    verse = callback_query.data.split("_")[1]
    if verse == "naruto":
        chars = [
            InlineKeyboardButton("Naruto Uzumaki", callback_data="char_naruto"),
            InlineKeyboardButton("Sasuke Uchiha", callback_data="char_sasuke"),
            InlineKeyboardButton("Kakashi Hatake", callback_data="char_kakashi")
        ]
    elif verse == "onepiece":
        chars = [
            InlineKeyboardButton("Luffy", callback_data="char_luffy"),
            InlineKeyboardButton("Zoro", callback_data="char_zoro"),
            InlineKeyboardButton("Sanji", callback_data="char_sanji")
        ]
    elif verse == "bleach":
        chars = [
            InlineKeyboardButton("Ichigo", callback_data="char_ichigo"),
            InlineKeyboardButton("Rukia", callback_data="char_rukia"),
            InlineKeyboardButton("Byakuya", callback_data="char_byakuya")
        ]
    keyboard = InlineKeyboardMarkup([[btn] for btn in chars])
    await callback_query.message.edit_caption(
        f"**{verse.capitalize()} verse selected!**\nNow choose your warrior:",
        reply_markup=keyboard
    )
    await callback_query.answer()

# Step 4: Character Chosen → Show Stats
@bot.on_callback_query(filters.regex("char_"))
async def final_character(client, callback_query):
    char = callback_query.data.split("_")[1].capitalize()
    stats = f"**{char} Selected!**\n\n**Level**: 1\n**Power**: 120\n**Defense**: 90\n**Speed**: 100\n\nLet the battles begin!"
    await callback_query.message.edit_caption(
        stats
    )
    await callback_query.answer("Warrior Selected!")

print("Bot is running...")
bot.run()