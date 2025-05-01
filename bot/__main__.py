from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Bot.db import init_db, add_user
import asyncio

# Init DB
init_db()

# Bot instance
app = Client(
    "waifu_guess_bot",
    api_id=123456,  # Replace with your actual api_id
    api_hash="your_api_hash",
    bot_token="your_bot_token"
)

# /start command
@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user = message.from_user
    add_user(user.id, user.username, user.first_name)

    # Send Goku sticker first
    sticker_msg = await message.reply_sticker("CAACAgUAAxkBAAEICFFmX_kX5f1JZNNgVK7WLPc6TcAdJgACnQIAApUo8VSVgyfSh-dAEi8E")

    # Wait then delete sticker
    await asyncio.sleep(2)
    await sticker_msg.delete()

    # Send welcome image with buttons
    await message.reply_photo(
        photo="https://telegra.ph/file/6da041da9edee75f2aafe.jpg",  # Replace with your image
        caption=f"**Welcome {user.first_name} to Waifu Guess World!**\nGuess waifus, collect, gift, and trade them!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Me to Group", url="https://t.me/YourBotUsername?startgroup=true")],
            [
                InlineKeyboardButton("👑 Owner", url="https://t.me/YourUsername"),
                InlineKeyboardButton("❓ Help", callback_data="help")
            ]
        ])
    )

# Run the bot
app.run()