from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api_id = int(input("25698862: "))
api_hash = input("7d7739b44f5f8c825d48cc6787889dbc: ")
bot_token = input("8068521367:AAFHqYZnf7DnsSWFpN8bk_ffJ5Qe3giRbNw: ")

bot = Client(
    "battle_game_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@bot.on_message(filters.command("start") & filters.private)
async def start_game(client, message):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Start Game", callback_data="start_game")]
        ]
    )
    await message.reply_photo(
        photo="https://files.catbox.moe/461mqe.jpg",
        caption="**Welcome to Battle Arena!**\nChoose your destiny and fight legendary enemies!",
        reply_markup=keyboard
    )

print("Bot is running...")
bot.run()