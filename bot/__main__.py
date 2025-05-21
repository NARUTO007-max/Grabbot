from pyrogram import Client, filters
from pyrogram.types import Message
from bot.db import waifu_col
from pymongo import MongoClient
from pyrogram import filters
from pyrogram.types import Message
import re
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import time
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import choice
from bot.db import waifu_col, get_all_groups
from config import OWNER_ID  # You define your owner ID here
from bot.db import waifu_col, add_waifu_to_user
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import time

# Bot setup
bot = Client(
    "waifu_bot",
    api_id=25698862,
    api_hash="7d7739b44f5f8c825d48cc6787889dbc",
    bot_token="7900777297:AAHOO4aS-Bx5WRScOVglWRWsa8m5n5vdwvQ"
)

start_time = time.time()

def get_uptime():
    seconds = int(time.time() - start_time)
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return f"{hours}h:{mins}m:{secs}s"

# --- START command handler ---
@bot.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    start = time.time()
    temp = await message.reply("Pinging...")
    ping = (time.time() - start) * 1000
    await temp.delete()

    await message.reply_photo(
        photo="https://files.catbox.moe/jejubs.jpg",
        caption=(
            "🌿 𝗚𝗥𝗘𝗘𝗧𝗜𝗡𝗚𝗦, 𝗜'𝗠 「ᴡᴀɪғᴜ ɢʀᴀʙʙᴇʀ ʙᴏᴛ」, 𝗡𝗜𝗖𝗘 𝗧𝗢 𝗠𝗘𝗘𝗧 𝗬𝗢𝗨!\n"
            "━━━━━━━━━━━━━━\n"
            "◎ 𝗪𝗛𝗔𝗧 𝗜 𝗗𝗢: 𝗜 𝗦𝗣𝗔𝗪𝗡 𝗪𝗔𝗜𝗙𝗨𝗦 𝗜𝗡 𝗬𝗢𝗨𝗥 𝗖𝗛𝗔𝗧.\n"
            "◎ 𝗧𝗢 𝗨𝗦𝗘 𝗠𝗘: 𝗔𝗗𝗗 𝗠𝗘 𝗧𝗢 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣 𝗔𝗡𝗗 𝗧𝗔𝗣 𝗛𝗘𝗟𝗣 𝗙𝗢𝗥 𝗗𝗘𝗧𝗔𝗜𝗟𝗦.\n"
            "━━━━━━━━━━━━━━\n"
            f"➛ 𝗣𝗜𝗡𝗚: {ping:.2f} ms\n"
            f"➛ 𝗨𝗣𝗧𝗜𝗠𝗘: {get_uptime()}"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ ADD ME ➕", url="https://t.me/YourBotUsername?startgroup=true")],
            [InlineKeyboardButton("🐉 Support group 🐉", url="https://t.me/animaction_world_in_2025"),
             InlineKeyboardButton("🍁 OWNER 🍁", url="https://t.me/Uzumaki_X_Naruto_6")],
            [InlineKeyboardButton("🛡️ HELP ⚡", callback_data="help"),
             InlineKeyboardButton("💲 REFRESH 💲", callback_data="refresh")]
        ])
    )

# --- Refresh Handler ---
@bot.on_callback_query(filters.regex("refresh"))
async def refresh_handler(client, query: CallbackQuery):
    start = time.time()
    temp = await query.message.reply("Refreshing...")
    ping = (time.time() - start) * 1000
    await temp.delete()

    await query.message.edit_caption(
        caption=(
            "🌿 𝗚𝗥𝗘𝗘𝗧𝗜𝗡𝗚𝗦, 𝗜'𝗠 「ᴡᴀɪғᴜ ɢʀᴀʙʙᴇʀ ʙᴏᴛ」, 𝗡𝗜𝗖𝗘 𝗧𝗢 𝗠𝗘𝗘𝗧 𝗬𝗢𝗨!\n"
            "━━━━━━━━━━━━━━\n"
            "◎ 𝗪𝗛𝗔𝗧 𝗜 𝗗𝗢: 𝗜 𝗦𝗣𝗔𝗪𝗡 𝗪𝗔𝗜𝗙𝗨𝗦 𝗜𝗡 𝗬𝗢𝗨𝗥 𝗖𝗛𝗔𝗧.\n"
            "◎ 𝗧𝗢 𝗨𝗦𝗘 𝗠𝗘: 𝗔𝗗𝗗 𝗠𝗘 𝗧𝗢 𝗚𝗥𝗢𝗨𝗣 𝗔𝗡𝗗 𝗨𝗦𝗘 𝗛𝗘𝗟𝗣 𝗕𝗨𝗧𝗧𝗢𝗡.\n"
            "━━━━━━━━━━━━━━\n"
            f"➛ 𝗣𝗜𝗡𝗚: {ping:.2f} ms\n"
            f"➛ 𝗨𝗣𝗧𝗜𝗠𝗘: {get_uptime()}"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ ADD ME ➕", url="https://t.me/YourBotUsername?startgroup=true")],
            [InlineKeyboardButton("🐉 Support group 🐉", url="https://t.me/animaction_world_in_2025"),
             InlineKeyboardButton("🍁 OWNER 🍁", url="https://t.me/Uzumaki_X_Naruto_6")],
            [InlineKeyboardButton("🛡️ HELP ⚡", callback_data="help"),
             InlineKeyboardButton("💲 REFRESH 💲", callback_data="refresh")]
        ])
    )
    await query.answer("Refreshed!")

# --- Help Handler ---
@bot.on_callback_query(filters.regex("help"))
async def help_handler(client, query: CallbackQuery):
    await query.message.edit_caption(
        caption=(
            "🛡️ **Help Menu**\n\n"
            "› Use me in groups to spawn random waifus.\n"
            "› Claim them before others do!\n"
            "› More coming soon...\n\n"
            "Use the buttons below to return."
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="baka")]
        ])
    )
    await query.answer("Help menu!")

@bot.on_message(filters.command("mywaifus"))
async def my_waifus(client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user = waifu_col.find_one({"user_id": user_id})

    if not user or not user.get("waifus"):
        await message.reply("You haven't claimed any waifus yet!")
        return

    waifus = user["waifus"]
    last_image = waifus[-1].get("image", None)
    
    anime_groups = {}
    for w in waifus:
        anime_groups.setdefault(w["anime"], []).append(w)

    text = f"**{user.get('username', user_name)}'s Harem - Page 1/1**\n\n"
    for anime, wlist in anime_groups.items():
        text += f"⌬ {anime} 〔{len(wlist)}〕\n"
        for w in wlist:
            text += f"◈⌠{w['rarity']}⌡ {w['id']} {w['name']} (x{w['count']})\n"
        text += "\n"

    if last_image:
        await message.reply_photo(
            photo=last_image,
            caption=text
        )
    else:
        await message.reply(text)

@bot.on_message(filters.command("fav"))
async def fav_waifu_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/fav <waifu_id>`", quote=True)

    try:
        waifu_id = int(message.command[1])
    except ValueError:
        return await message.reply("Waifu ID must be a number.", quote=True)

    user_id = message.from_user.id

    user_data = waifu_col.find_one({"user_id": user_id})
    if not user_data or "waifus" not in user_data:
        return await message.reply("You don't have any waifus yet.", quote=True)

    for waifu in user_data["waifus"]:
        if waifu.get("id") == waifu_id:
            waifu_col.update_one(
                {"user_id": user_id},
                {"$set": {"favorite_waifu_id": waifu_id}}
            )
            return await message.reply(f"⭐ Waifu `{waifu_id}` has been set as your favorite!", quote=True)

    await message.reply("Waifu ID not found in your harem.", quote=True)

drop_time_settings = {}  # Use MongoDB in production

@bot.on_message(filters.command("changetime") & filters.user(7576729648))
async def change_time_handler(client, message):
    try:
        time_arg = message.text.split()[1]
        drop_time_settings["time"] = time_arg
        # MongoDB: store per-group time config
        await message.reply(f"✅ Drop time updated to {time_arg}")
    except:
        await message.reply("Usage: /changetime 1m / 30s / 2m")

# --- Upload Command (For Admins Only) ---
@bot.on_message(filters.command("upload") & filters.user(7576729648))
async def upload_waifu(client, message: Message):
    try:
        # Extract arguments from message
        args_text = message.text.split(None, 1)[1]
        args = dict(re.findall(r"(\w+)=([^\s]+)", args_text))

        name = args.get("name", "").replace("_", " ")
        rarity = args.get("rarity", "").capitalize()
        source = args.get("source", "").replace("_", " ")
        image = args.get("image", "")

        rarity_emojis = {
            "Common": "⚪️",
            "Uncommon": "🟢",
            "Rare": "🔵",
            "Epic": "🟣",
            "Legendary": "🟡",
            "Mythical": "🟠",
            "Limited": "🔮"
        }

        emoji = rarity_emojis.get(rarity, "⚪️")

        waifu_data = {
            "name": name,
            "rarity": rarity,
            "source": source,
            "image": image,
            "emoji": emoji
        }

        waifu_col.insert_one(waifu_data)

        await message.reply(
            f"✅ **Waifu Uploaded Successfully!**\n\n"
            f"{emoji} **Name:** {name}\n"
            f"📚 **Source:** {source}\n"
            f"✨ **Rarity:** {rarity}"
        )

    except Exception as e:
        await message.reply(f"❌ Failed to upload waifu.\nError: `{str(e)}`")# In-memory store for last waifu drop per chat
last_waifu_drop = {}  # {chat_id: {"waifu": {...}, "time": timestamp, "grabbed": False}}

@bot.on_message(filters.command("grab") & filters.group)
async def grab_waifu(_, message):
    user_id = message.from_user.id
    group_id = message.chat.id

    current_waifu = waifu_drops.get(group_id)
    if not current_waifu:
        return await message.reply("No waifu is currently available to grab.")

    # Check if already grabbed
    if current_waifu.get("grabbed_by"):
        return await message.reply("This waifu has already been grabbed.")

    # Set the waifu as grabbed
    current_waifu["grabbed_by"] = user_id
    waifu_drops[group_id] = current_waifu

    # Save to DB
    waifu_doc = {
        "user_id": user_id,
        "waifu_id": current_waifu["id"],
        "name": current_waifu["name"],
        "rarity": current_waifu["rarity"],
        "image": current_waifu["image"],
        "count": 1,
        "anime": current_waifu.get("anime", "Unknown")
    }

    existing = await waifu_collection.find_one({
        "user_id": user_id,
        "waifu_id": current_waifu["id"]
    })

    if existing:
        await waifu_collection.update_one(
            {"_id": existing["_id"]},
            {"$inc": {"count": 1}}
        )
    else:
        await waifu_collection.insert_one(waifu_doc)

    # Format rarity with emoji
    emoji = {
        "Common": "⚪️",
            "Uncommon": "🟢",
            "Rare": "🔵",
            "Epic": "🟣",
            "Legendary": "🟡",
            "Mythical": "🟠",
            "Limited": "🔮"
    }.get(current_waifu["rarity"], "❔")

    text = (
        f"**{emoji} Grab Success!**\n\n"
        f"**Name:** {current_waifu['name']}\n"
        f"**Rarity:** {current_waifu['rarity']}\n"
        f"**Anime:** {current_waifu.get('anime', 'Unknown')}\n"
        f"**Waifu ID:** `{current_waifu['id']}`\n"
    )

    buttons = [
        [InlineKeyboardButton("My Waifus", callback_data="mywaifus")]
    ]

    await message.reply_photo(current_waifu["image"], caption=text, reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_message(filters.command("fdrop") & filters.user(7576729648))
async def fdrop_handler(client, message):
    waifu_list = list(waifu_col.aggregate([{"$unwind": "$waifus"}, {"$replaceRoot": {"newRoot": "$waifus"}}]))
    if not waifu_list:
        return await message.reply("❌ No waifus in database.")

    waifu = choice(waifu_list)
    caption = (
        f"🔴 ᴀ waifu ʜᴀs ᴀᴘᴘᴇᴀʀᴇᴅ!\n"
        f"ᴀᴅᴅ ʜɪᴍ ᴛᴏ ʏᴏᴜʀ ʜᴀʀᴇᴍ ʙʏ sᴇɴᴅɪɴɢ:\n"
        f"/grab {waifu['name']}"
    )

    groups = get_all_groups()
    for group_id in groups:
        try:
            await client.send_photo(
                group_id,
                photo=waifu["image"],
                caption=caption
            )
        except Exception as e:
            print(f"Failed to send to {group_id}: {e}")

    await message.reply("✅ Waifu dropped in all groups!")

# --- Start Bot ---
if __name__ == "__main__":
    print("[BOT STARTED||💲💲💲]")
    bot.run()