from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db import init_db, add_user, get_user_waifus, get_waifu_by_user, update_waifu_quantity, add_or_update_waifu
import asyncio
import sqlite3

api_id = 25698862
api_hash = "7d7739b44f5f8c825d48cc6787889dbc"
bot_token = "7608107574:AAH_PGTsl7ua9IY9C1GQOz5qdU8XjXATH80"

app = Client("hinata_waifu_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

init_db()

RARITY_EMOJIS = {
    "Common": "⚪️",
    "Rare": "🔵",
    "Epic": "🟣",
    "Legendary": "🟡",
    "Special Edition": "💮"
}

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

# Start the bot
if __name__ == "__main__":
    app.run()