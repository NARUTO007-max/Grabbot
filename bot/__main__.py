from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.db import init_db, add_user
import asyncio

# Init DB
init_db()

# Bot instance
app = Client(
    "waifu_guess_bot",
    api_id=25698862,  # Replace with your actual api_id
    api_hash="7d7739b44f5f8c825d48cc6787889dbc",
    bot_token="7608107574:AAH_PGTsl7ua9IY9C1GQOz5qdU8XjXATH80"
)

# /start command
@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user = message.from_user
    add_user(user.id, user.username, user.first_name)

    # Send Goku sticker first
    sticker_msg = await message.reply_sticker("CAACAgUAAxkBAfcaNmgTo-RkdWFjNVSvGLHpOdwBzsLQAALYDwAC82qpVcmJwWw59RlONgQ")

    # Wait then delete sticker
    await asyncio.sleep(2)
    await sticker_msg.delete()

    # Send welcome image with updated caption and buttons
    await message.reply_photo(
        photo="https://files.catbox.moe/461mqe.jpg",  # Replace with your image
        caption=f"""
*ʜᴇʟʟᴏ...*

*ɪ'ᴍ ʜɪɴᴀᴛᴀ ʏᴏᴜʀ ᴡᴀɪғᴜ ᴄʜᴀʀᴀᴄᴛᴇʀ ɢᴜᴇss ʙᴏᴛ.....

ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ɪ ᴡɪʟʟ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ...

ᴛᴀᴘ ᴏɴ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ sᴇᴇ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs...

ᴍᴜsᴛ Jᴏɪɴ :- @animaction_world_in_2025
        """,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Me to Group", url="https://t.me/HinataXSupportbot?startgroup=true")],
            [
                InlineKeyboardButton("👑 Owner", url="https://t.me/Uzumaki_X_Naruto_6"),
                InlineKeyboardButton("❓ Help", callback_data="help")
            ]
        ])
    )

# Run the bot
app.run()