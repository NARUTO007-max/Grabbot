from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.db import init_db, add_user
import asyncio

# Init DB
init_db()

# Bot instance
app = Client(
    "waifu_guess_bot",
    api_id=25698862,
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
        photo="https://files.catbox.moe/461mqe.jpg",
        caption=f"""
*ʜᴇʟʟᴏ...*

*ɪ'ᴍ ʜɪɴᴀᴛᴀ ʏᴏᴜʀ ᴡᴀɪғᴜ ᴄʜᴀʀᴀᴄᴛᴇʀ ɢᴜᴇss ʙᴏᴛ.....

ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ɪ ᴡɪʟʟ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ...

ᴛᴀᴘ ᴏɴ ʙᴜᴛᴛᴏɴs ғᴏʀ ᴍᴏʀᴇ...

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

RARITY_EMOJIS = {
    "orange": "🟠",
    "yellow": "🟡",
    "red": "🔴"
}

# /mywaifu command
@app.on_message(filters.command("mywaifu"))
async def mywaifu_command(client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    waifus = get_user_waifus(user_id)

    if not waifus:
        await message.reply(f"**{first_name}** has no waifus yet!")
        return

    # Group by series
    series_dict = {}
    for entry in waifus:
        series = entry["series"]
        if series not in series_dict:
            series_dict[series] = []
        series_dict[series].append(entry)

    text = f"*{first_name}'s Harem*\n"
    for series, chars in series_dict.items():
        total = sum(c["quantity"] for c in chars)
        text += f"\n⥱ {series} {total}/{len(chars)}\n"
        text += "⚋" * 15 + "\n"
        for c in chars:
            emoji = RARITY_EMOJIS.get(c["rarity"], "")
            group_tag = " [👥]" if c["is_group"] else ""
            text += f"➥ {c['char_id']} | {emoji} | {c['name']}{group_tag} x{c['quantity']}\n"
        text += "⚋" * 15 + "\n"

    # Add pagination buttons (for now static, later dynamic)
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("1x⬅️", callback_data="prev_page_1"),
        InlineKeyboardButton("1/1", callback_data="page_info"),
        InlineKeyboardButton("1x➡️", callback_data="next_page_1")
    ]])

    await message.reply(text, reply_markup=keyboard)

# /gift command 
@app.on_message(filters.command("gift"))
async def gift_waifu(client, message: Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.reply("**Usage:** `/gift <waifu_id> <@username or user_id>`")
        return

    sender_id = message.from_user.id
    waifu_id = args[1]
    target_raw = args[2]

    # Resolve user ID
    if target_raw.startswith("@"):
        try:
            target_user = await client.get_users(target_raw)
            receiver_id = target_user.id
        except Exception:
            return await message.reply("❌ Couldn't find that user.")
    else:
        try:
            receiver_id = int(target_raw)
        except ValueError:
            return await message.reply("❌ Invalid user ID.")

    if receiver_id == sender_id:
        return await message.reply("❌ You can't gift a waifu to yourself!")

    # Check sender has the waifu
    sender_has = get_waifu_by_user(sender_id, waifu_id)
    if not sender_has or sender_has["quantity"] < 1:
        return await message.reply("❌ You don't own this waifu!")

    # Deduct from sender
    update_waifu_quantity(sender_id, waifu_id, -1)

    # Add to receiver
    add_or_update_waifu(receiver_id, sender_has)

    await message.reply(
        f"✅ Successfully gifted `{waifu_id}` ({sender_has['name']}) to [{receiver_id}](tg://user?id={receiver_id})!"
    )

def get_waifu_by_user(user_id, char_id):
    conn = sqlite3.connect("waifus.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM waifus WHERE user_id = ? AND char_id = ?", (user_id, char_id))
    result = cur.fetchone()
    conn.close()
    return dict(result) if result else None

def update_waifu_quantity(user_id, char_id, delta):
    conn = sqlite3.connect("waifus.db")
    cur = conn.cursor()
    cur.execute("UPDATE waifus SET quantity = quantity + ? WHERE user_id = ? AND char_id = ?", (delta, user_id, char_id))
    conn.commit()
    conn.close()

def add_or_update_waifu(user_id, waifu_data):
    conn = sqlite3.connect("waifus.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM waifus WHERE user_id = ? AND char_id = ?", (user_id, waifu_data["char_id"]))
    exists = cur.fetchone()
    if exists:
        cur.execute("UPDATE waifus SET quantity = quantity + 1 WHERE user_id = ? AND char_id = ?", (user_id, waifu_data["char_id"]))
    else:
        cur.execute("INSERT INTO waifus (user_id, series, char_id, rarity, name, quantity, is_group) VALUES (?, ?, ?, ?, ?, ?, ?)", (
            user_id,
            waifu_data["series"],
            waifu_data["char_id"],
            waifu_data["rarity"],
            waifu_data["name"],
            1,
            waifu_data["is_group"]
        ))
    conn.commit()
    conn.close()

# /trade command 
@app.on_message(filters.command("trade"))
async def trade_request_handler(client, message: Message):
    args = message.text.split()
    if len(args) != 4:
        return await message.reply("**Usage:** `/trade <your_waifuid> <partner_waifuid> <@username>`")

    sender_id = message.from_user.id
    your_waifuid = args[1]
    partner_waifuid = args[2]
    partner_raw = args[3]

    try:
        partner = await client.get_users(partner_raw)
        partner_id = partner.id
    except:
        return await message.reply("❌ Partner not found.")

    if partner_id == sender_id:
        return await message.reply("❌ You can't trade with yourself.")

    # Check waifu ownerships
    your_waifu = get_waifu_by_user(sender_id, your_waifuid)
    partner_waifu = get_waifu_by_user(partner_id, partner_waifuid)

    if not your_waifu or your_waifu["quantity"] < 1:
        return await message.reply("❌ You don't own this waifu.")

    if not partner_waifu or partner_waifu["quantity"] < 1:
        return await message.reply("❌ Partner doesn't own that waifu.")

    # Send trade request to partner
    trade_msg = await message.reply(
        f"👥 Trade Request Sent to [{partner.first_name}](tg://user?id={partner.id})\n\n"
        f"**{message.from_user.first_name}** wants to trade:\n\n"
        f"• `{your_waifuid}` → {your_waifu['name']}\n"
        f"• `{partner_waifuid}` ← {partner_waifu['name']}\n\n"
        "Do you accept?",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Accept", callback_data=f"accept_trade|{sender_id}|{your_waifuid}|{partner_waifuid}"),
                InlineKeyboardButton("❌ Reject", callback_data="reject_trade")
            ]
        ])
    )

@app.on_callback_query(filters.regex("accept_trade"))
async def accept_trade_callback(client, callback_query):
    data = callback_query.data.split("|")
    sender_id = int(data[1])
    your_waifuid = data[2]
    partner_waifuid = data[3]
    partner_id = callback_query.from_user.id

    # Double check both still own the waifus
    your_waifu = get_waifu_by_user(sender_id, your_waifuid)
    partner_waifu = get_waifu_by_user(partner_id, partner_waifuid)

    if not your_waifu or your_waifu["quantity"] < 1 or not partner_waifu or partner_waifu["quantity"] < 1:
        await callback_query.message.edit("❌ Trade failed. One of the waifus is no longer available.")
        return

    # Update DB: exchange
    update_waifu_quantity(sender_id, your_waifuid, -1)
    add_or_update_waifu(partner_id, your_waifu)

    update_waifu_quantity(partner_id, partner_waifuid, -1)
    add_or_update_waifu(sender_id, partner_waifu)

    await callback_query.message.edit(
        f"✅ Trade Successful!\n\n"
        f"• {your_waifu['name']} → {callback_query.from_user.first_name}\n"
        f"• {partner_waifu['name']} → [User](tg://user?id={sender_id})"
    )

@app.on_callback_query(filters.regex("reject_trade"))
async def reject_trade_callback(client, callback_query):
    await callback_query.message.edit("❌ Trade Rejected.")

# /upload and /guess command 
RARITY_MAP = {"1": "🟢", "2": "🟠", "3": "🟡", "4": "🔴", "5": "🟣"}

guess_data = {}  # temp memory, DB recommended for real usage

@app.on_message(filters.command("upload"))
async def upload_handler(client, message: Message):
    args = message.text.split(" ", 4)
    if len(args) != 5:
        return await message.reply("**Usage:** `/upload <image_url> <anime_name> <character_name> <rarity_no>`")

    image_url = args[1]
    anime = args[2].replace("_", " ")
    name = args[3].replace("_", " ")
    rarity_no = args[4]

    rarity_emoji = RARITY_MAP.get(rarity_no, "❓")
    if rarity_emoji == "❓":
        return await message.reply("❌ Invalid rarity number. Use 1-5.")

    # Generate unique ID
    char_id = f"{random.randint(10000,99999)}"
    guess_data[char_id] = {
        "name": name.lower(),
        "anime": anime,
        "rarity": rarity_emoji,
        "guessed_by": None,
        "coins": 40,
    }

    await client.send_photo(
        chat_id=message.chat.id,
        photo=image_url,
        caption=f"""💫 A Legendary character has emerged!
Guess their name with `/guess {char_id} <name>` to make them yours! 🏆""",
        parse_mode="markdown"
    )

@app.on_message(filters.command("guess"))
async def guess_handler(client, message: Message):
    args = message.text.split(" ", 2)
    if len(args) != 3:
        return await message.reply("**Usage:** `/guess <id> <character_name>`")

    waifu_id = args[1]
    guess = args[2].strip().lower()

    waifu = guess_data.get(waifu_id)

    if not waifu:
        return await message.reply("❌ Invalid or expired waifu ID.")

    if waifu["guessed_by"]:
        return await message.reply("⚠️ This character has already been guessed.")

    if guess != waifu["name"]:
        return await message.reply("❌ Wrong guess. Try again!")

    waifu["guessed_by"] = message.from_user.id
    username = message.from_user.first_name
    coins = waifu["coins"]

    # Send rewards message + character reveal
    await message.reply(
        f"🎉 Congrats! You've earned {coins} dazzling coins for guessing correctly! 💰"
    )

    await message.reply(
        f"**{username}** 🎊 You guessed the character!\n\n"
        f"🍁 Name: {waifu['name'].title()}\n"
        f"⛩ Anime: {waifu['anime']}\n"
        f"🎐 Rarity: {waifu['rarity']}\n\n"
        "This character is now in your harem! Use /mycollection to see your harem.",
        parse_mode="markdown"
    )

# /mycollection command 
@app.on_message(filters.command("mycollection"))
async def mycollection_handler(client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    waifus = user_waifus.get(user_id, [])

    if not waifus:
        return await message.reply("❌ You haven't earned any waifus yet. Start guessing using /guess!")

    # Group by anime
    grouped = defaultdict(list)
    for w in waifus:
        grouped[w['anime']].append(w)

    # Format output
    response = f"**{username}**'s Harem\n\n"
    for anime, chars in grouped.items():
        response += f"⥱ {anime} {len(chars)}/{len(chars)}\n"
        response += "⚋" * 15 + "\n"
        for w in chars:
            response += f"➥ {w['id']} | {w['rarity']} | {w['name']} x1\n"
        response += "⚋" * 15 + "\n\n"

    await message.reply(response)

@app.on_message(filters.command("mycollection"))
async def mycollection_handler(client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    conn = sqlite3.connect("waifus.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM waifus WHERE user_id = ?", (user_id,))
    all_waifus = cur.fetchall()
    conn.close()

    if not all_waifus:
        return await message.reply(f"**{first_name}**, you haven't collected any waifus yet!")

    total_waifus = sum([w["quantity"] for w in all_waifus])
    unique_waifus = len(all_waifus)

    # Count by rarity
    rarity_count = {"orange": 0, "yellow": 0, "red": 0}
    for w in all_waifus:
        rarity_count[w["rarity"]] += w["quantity"]

    await message.reply(
        f"**{first_name}'s Collection Summary:**\n\n"
        f"➤ Total Waifus: `{total_waifus}`\n"
        f"➤ Unique Waifus: `{unique_waifus}`\n\n"
        f"🔴 Red: `{rarity_count['red']}`\n"
        f"🟡 Yellow: `{rarity_count['yellow']}`\n"
        f"🟠 Orange: `{rarity_count['orange']}`"
    )

# Run the bot
app.run()