from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from bot.db import add_user, is_premium
import asyncio
from bot.db import add_premium
from pyrogram.errors import UserNotParticipant

app = Client("QTBot", api_id=21218274, api_hash="3474a18b61897c672d315fb330edb213", bot_token="7207574948:AAGRV7Te9gcinmy9hLnPvAOiEzcOYgllDns")

QR_IMAGE = "https://files.catbox.moe/cqj1l0.jpg"
OWNER_USERNAME = "@Uzumaki_X_Naruto_6"

@app.on_message(filters.command("start"))
async def start(_, m: Message):
    user_id = m.from_user.id
    add_user(user_id)
    
    text = f"""
Hᴇʟʟᴏ {m.from_user.mention},

ɪ ᴀᴍ ᴀᴅᴠᴀɴᴄᴇᴅ 【ꜱᴘᴀᴍ & ʀᴀɪᴅ】ʙᴏᴛ ᴡɪᴛʜ ᴄʟᴏɴᴇ ғᴇᴀᴛᴜʀᴇ

⚡ Cʀᴇᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ Qᴛ Bᴏᴛ
"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Join Owner", url=f"https://t.me/{OWNER_USERNAME}")],
        [InlineKeyboardButton("⚙️ Get Premium", callback_data="get_premium")],
        [InlineKeyboardButton("🛠 Help", callback_data="help")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ])
    await m.reply_photo(QR_IMAGE, caption=text, reply_markup=keyboard)

@app.on_callback_query()
async def callback_query_handler(_, query):
    if query.data == "get_premium":
        text = f"✨ 30Rs = 1 Month Premium\n\nUPI: `vivekrajroy705@oksbi`\n\nSend screenshot after payment."
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📷 Send Screenshot", url=f"https://t.me/{OWNER_USERNAME}")],
            [InlineKeyboardButton("🔙 Back", callback_data="start")]
        ])
        await query.message.edit_caption(text, reply_markup=keyboard)

    elif query.data == "help":
        text = "**QT Bot Commands**\n\n/raid [count] [text]\n/spam [@user] [count] [text]\n/about\n/start"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]])
        await query.message.edit_caption(text, reply_markup=keyboard)

    elif query.data == "about":
        text = f"""
🤖 ᴍʏ ɴᴀᴍᴇ: QT BOT
📝 ʟᴀɴɢᴜᴀɢᴇ: Python 3
📚 ʟɪʙʀᴀʀʏ: Pyrogram
🧑🏻‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ: @{OWNER_USERNAME}
"""
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]])
        await query.message.edit_caption(text, reply_markup=keyboard)

@app.on_message(filters.command("raid") & filters.private)
async def raid(_, m):
    user_id = m.from_user.id
    if not is_premium(user_id):
        return await m.reply("❌ Premium required. Use /start and click 'Get Premium'.")

    try:
        count = int(m.command[1])
        text = " ".join(m.command[2:])
    except:
        return await m.reply("Usage: /raid [count] [text]")

    for _ in range(count):
        await m.reply(text)
        await asyncio.sleep(0.4)

@app.on_message(filters.command("spam") & filters.private)
async def spam(_, m):
    user_id = m.from_user.id
    if not is_premium(user_id):
        return await m.reply("❌ Premium required.")

    try:
        target = m.command[1]
        count = int(m.command[2])
        text = " ".join(m.command[3:])
    except:
        return await m.reply("Usage: /spam [@user] [count] [text]")

    for _ in range(count):
        await m.reply(f"{target} {text}")
        await asyncio.sleep(0.4)

@app.on_message(filters.command("auth") & filters.user("7576729648"))
async def auth(_, m):
    if len(m.command) < 2:
        return await m.reply("Usage: /auth @username")

    try:
        username = m.command[1].replace("@", "")
        user = await app.get_users(username)
        add_premium(user.id)
        await m.reply(f"✅ Premium access unlocked for {user.mention}")
    except Exception as e:
        await m.reply(f"Error: {e}")

app.run()