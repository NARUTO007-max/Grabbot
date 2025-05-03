from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.db import init_db, add_user, get_user_waifus, get_waifu_by_user, update_waifu_quantity, add_or_update_waifu
import asyncio
import sqlite3

api_id = 25698862
api_hash = "7d7739b44f5f8c825d48cc6787889dbc"
bot_token = "7608107574:AAH_PGTsl7ua9IY9C1GQOz5qdU8XjXATH80"

app = Client("hinata_waifu_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Database init
conn = sqlite3.connect("waifubot.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS waifus (
    waifu_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    rarity TEXT,
    description TEXT,
    photo_id TEXT
)""")
conn.commit()

user_upload_state = {}

@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user = message.from_user
    add_user(user.id, user.username, user.first_name)

    sticker = await message.reply_sticker("CAACAgUAAxkBAfcaNmgTo-RkdWFjNVSvGLHpOdwBzsLQAALYDwAC82qpVcmJwWw59RlONgQ")
    await asyncio.sleep(2)
    await sticker.delete()

    await message.reply_photo(
        photo="https://files.catbox.moe/461mqe.jpg",
        caption="""
*ʜᴇʟʟᴏ...*

*ɪ'ᴍ ʜɪɴᴀᴛᴀ ʏᴏᴜʀ ᴡᴀɪғᴜ ᴄʜᴀʀᴀᴄᴛᴇʀ ɢᴜᴇss ʙᴏᴛ.....*

ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ɪ ᴡɪʟʟ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ...

ᴍᴜsᴛ Jᴏɪɴ :- @animaction_world_in_2025
        """,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("〔 ＋ ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ 〕", url="https://t.me/HinataXSupportbot?startgroup=true")],
            [
                InlineKeyboardButton("🥀 ᴏᴡɴᴇʀ 🥀", url="https://t.me/Uzumaki_X_Naruto_6"),
                InlineKeyboardButton("🥀 ɢʀᴏᴜᴘ 🥀", url="https://t.me/animaction_world_in_2025")
            ]
        ])
    )

@app.on_message(filters.command("mywaifu"))
async def mywaifu_command(client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    waifus = get_user_waifus(user_id)

    if not waifus:
        return await message.reply(f"**{first_name}** has no waifus yet!")

    series_dict = {}
    for w in waifus:
        series_dict.setdefault(w["series"], []).append(w)

    text = f"*{first_name}'s Harem*\n"
    for series, chars in series_dict.items():
        text += f"\n⥱ {series} ({len(chars)} waifus)\n"
        text += "⚋" * 15 + "\n"
        for c in chars:
            emoji = RARITY_EMOJIS.get(c["rarity"], "")
            group_tag = " [👥]" if c["is_group"] else ""
            text += f"➥ {c['char_id']} | {emoji} | {c['name']}{group_tag} x{c['quantity']}\n"
        text += "⚋" * 15 + "\n"

    await message.reply(text)

@app.on_message(filters.command("gift"))
async def gift_command(client, message: Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        return await message.reply("Usage: `/gift <waifu_id> <@user>`")

    sender_id = message.from_user.id
    waifu_id = parts[1]
    receiver_username = parts[2]

    try:
        receiver = await client.get_users(receiver_username)
    except:
        return await message.reply("User not found.")

    if receiver.id == sender_id:
        return await message.reply("❌ Can't gift yourself!")

    waifu = get_waifu_by_user(sender_id, waifu_id)
    if not waifu or waifu["quantity"] < 1:
        return await message.reply("❌ You don't own this waifu.")

    update_waifu_quantity(sender_id, waifu_id, -1)
    add_or_update_waifu(receiver.id, waifu)

    await message.reply(f"✅ Gifted `{waifu_id}` ({waifu['name']}) to [{receiver.first_name}](tg://user?id={receiver.id})!")

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Dict

# Dictionary to store pending trades
pending_trades: Dict[str, Dict] = {}

# Assuming we have a database or in-memory structure to store waifus
# Function to get waifu by user ID and waifu ID
def get_waifu_by_user(user_id, waifu_id):
    # This should fetch waifu data from the database based on the user and waifu IDs
    # Return None if not found
    pass

# Function to update waifu quantity after trade
def update_waifu_quantity(user_id, waifu_id, quantity_change):
    # This should update the waifu quantity in the database
    pass

# Function to add or update waifu for the user
def add_or_update_waifu(user_id, waifu_data):
    # Add or update waifu data in the database
    pass

@app.on_message(filters.command("trade"))
async def trade_command(client, message: Message):
    parts = message.text.split()
    if len(parts) < 4:
        return await message.reply("Usage:\n`/trade <your_waifu_id> <@username> <their_waifu_id>`")

    user1 = message.from_user
    waifu1_id = parts[1]
    target_username = parts[2]
    waifu2_id = parts[3]

    try:
        user2 = await client.get_users(target_username)
    except:
        return await message.reply("User not found!")

    if user1.id == user2.id:
        return await message.reply("❌ Can't trade with yourself.")

    # Get waifu details for both users
    waifu1 = get_waifu_by_user(user1.id, waifu1_id)
    waifu2 = get_waifu_by_user(user2.id, waifu2_id)

    if not waifu1:
        return await message.reply(f"You don't own waifu `{waifu1_id}`.")
    if not waifu2:
        return await message.reply(f"{user2.first_name} doesn't own waifu `{waifu2_id}`.")

    trade_id = f"{user1.id}_{user2.id}_{waifu1_id}_{waifu2_id}"
    pending_trades[trade_id] = {
        "user1": user1.id,
        "user2": user2.id,
        "waifu1": waifu1,
        "waifu2": waifu2
    }

    await message.reply(
        f"📦 Trade Proposal Sent To [{user2.first_name}](tg://user?id={user2.id})\n\n"
        f"• {user1.first_name} wants to trade:\n"
        f"`{waifu1_id}` ({waifu1['name']})\n"
        f"⬌\n"
        f"`{waifu2_id}` ({waifu2['name']}) from {user2.first_name}",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Accept", callback_data=f"accept_trade|{trade_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_trade|{trade_id}")
        ]])
    )

@app.on_callback_query(filters.regex("^(accept_trade|reject_trade)\|"))
async def handle_trade_callback(client, callback_query: CallbackQuery):
    data = callback_query.data.split("|")
    action = data[0]
    trade_id = data[1]

    trade = pending_trades.get(trade_id)
    if not trade:
        return await callback_query.answer("This trade has expired or is invalid.", show_alert=True)

    user2_id = callback_query.from_user.id
    if user2_id != trade["user2"]:
        return await callback_query.answer("You're not authorized for this trade.", show_alert=True)

    if action == "reject_trade":
        del pending_trades[trade_id]
        return await callback_query.edit_message_text("❌ Trade rejected!")

    # Proceed with the trade (swap waifus)
    w1 = trade["waifu1"]
    w2 = trade["waifu2"]
    user1 = trade["user1"]
    user2 = trade["user2"]

    # Deduct one waifu each
    update_waifu_quantity(user1, w1["char_id"], -1)
    update_waifu_quantity(user2, w2["char_id"], -1)

    # Add the other waifu to each user
    add_or_update_waifu(user1, w2)
    add_or_update_waifu(user2, w1)

    del pending_trades[trade_id]
    await callback_query.edit_message_text("✅ Trade successful! Waifus exchanged.")

@app.on_message(filters.command("upload") & filters.user([7019600964]))
async def upload_waifu(app, message: Message):
    try:
        # Command format: /upload image_url anime_name character_name rarity
        if len(message.command) < 5:
            return await message.reply(
                "❌ Format galat hai!\nUse: `/upload image_url anime_name character_name rarity (1-5)`",
                quote=True
            )

        image_url = message.command[1]
        anime_name = message.command[2]
        character_name = message.command[3]
        rarity_input = message.command[4]

        if not rarity_input.isdigit() or not (1 <= int(rarity_input) <= 5):
            return await message.reply("❌ Rarity 1 se 5 ke beech number hona chahiye.", quote=True)

        rarity_num = int(rarity_input)
        rarity_emojis = {
            1: "⚪",
            2: "🟢",
            3: "🟣",
            4: "🔴",
            5: "💮"
        }
        rarity_display = rarity_emojis[rarity_num]

        caption = (
            f"🌟 Pʀᴇᴘᴀʀᴇ Fᴏʀ A Tʜʀɪʟʟ! A ʙʀᴀɴᴅ-Nᴇᴡ 🔮 Limited Edition Cʜᴀʀᴀᴄᴛᴇʀ Hᴀs Eᴍᴇʀɢᴇᴅ!\n"
            f"Qᴜɪᴄᴋ, Hᴇᴀᴅ Tᴏ /guess Tᴏ Rᴇᴠᴇᴀʟ Tʜᴇ Cʜᴀʀᴀᴄᴛᴇʀ's Nᴀᴍᴇ Aɴᴅ Aᴅᴅ Iɴ Yᴏᴜʀ Hᴀʀᴇᴍ!\n\n"
            f"Anime: `{anime_name}`\nRarity: `{rarity_display}`"
        )

        await app.send_photo(
            chat_id=message.chat.id,
            photo=image_url,
            caption=caption
        )

        await message.reply("✅ Waifu uploaded successfully!", quote=True)

    except Exception as e:
        await message.reply(f"❌ Error: `{e}`", quote=True)

# Start the bot
if __name__ == "__main__":
    app.run()