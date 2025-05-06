import sys
from pyrogram import idle
from datetime import datetime
from urllib.parse import quote_plus
import random
import os
import time
import asyncio
import logging
from datetime import datetime
from pyrogram.enums import ChatType, ParseMode
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, AUCTION_GROUP_LINK, AUCTION_CHANNEL_ID, AUCTION_CHANNEL_LINK, COOLDOWN_TIME, OWNER_IDS, APPROVAL_GROUP_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pymongo import MongoClient
from AB.db import (
    users_collection,
    admins_collection,
    pending_submissions,
    cooldowns_collection,
    submissions_collection,
    approved_items_collection,
    bids_collection,
    save_submission_to_db,
    get_submission_from_db,
    get_user,
    add_user,
    update_user_stats,
    is_admin,
    add_admin,
    remove_admin,
    set_cooldown,
    get_cooldown,
    add_submission,
    place_bid
)
from bot import bot


# 🔹 Profile Templates (Template Number: Image Link)
profile_templates = {
    1: "https://files.catbox.moe/a8ud2n.jpg",
    2: "https://files.catbox.moe/jgjfjv.jpg",
    3: "https://files.catbox.moe/l46mcp.jpg",
    4: "https://files.catbox.moe/7mcf3g.jpg",
    5: "https://files.catbox.moe/rl6o0z.jpg",
    6: "https://files.catbox.moe/j309ys.jpg",
    7: "https://files.catbox.moe/rapqog.jpg",
    8: "https://files.catbox.moe/up2yq5.jpg",
    9: "https://files.catbox.moe/ata5gt.jpg",
    10: "https://files.catbox.moe/m3vtbn.jpg",
    11: "https://files.catbox.moe/wjx1eq.jpg",
    12: "https://files.catbox.moe/2u8gsa.jpg",
    13: "https://files.catbox.moe/a7pitn.jpg",
    14: "https://files.catbox.moe/ulkl4s.jpg",
    15: "https://files.catbox.moe/wskaum.jpg",
16: "https://files.catbox.moe/62uskb.jpg",
17: "https://files.catbox.moe/oo7kjv.jpg",
18: "https://files.catbox.moe/v2xf87.jpg",
}

default_profile_image = "https://files.catbox.moe/a8ud2n.jpg"  # default image
user_templates = {}  # user_id: template_number


@bot.on_message(filters.command("profile"), group=5)
async def profile_command(bot, message):
    user = message.from_user
    name = user.first_name or "N/A"
    username = f"@{user.username}" if user.username else "N/A"
    userid = user.id

    # Dummy data (replace with actual database values)
    total_shiny = await approved_items_collection.count_documents({"user_id": userid, "type": "shiny"})
    total_legendary = await approved_items_collection.count_documents({"user_id": userid, "type": "legendary"})
    total_non_legendary = await approved_items_collection.count_documents({"user_id": userid, "type": "non-legendary"})
    total_tms = 0
    total_teams = 0
    total_approved = total_shiny + total_legendary + total_non_legendary + total_tms + total_teams
    approved_ratio = f"{(total_approved / (total_approved + 0)) * 100:.2f}%" if total_approved > 0 else "0%"



    caption = f"""(VERIFIED ✅)

★ PROFILE ★
═════════════════════

➤ Name: {name}
➤ Username: {username}
➤ User ID: {userid}

──────────────
Total Approved Items:

➤ Shiny: {total_shiny}
➤ Legendary: {total_legendary}
➤ Non-Legendary: {total_non_legendary}

──────────────
➤ Total Approved : {total_approved}
──────────────
➤ Approved Ratio: {approved_ratio}
──────────────
"""

    selected_template = user_templates.get(userid, 0)
    profile_image = profile_templates.get(selected_template, default_profile_image)

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Close", callback_data="close_profile"),
                InlineKeyboardButton("Change Template", callback_data="change_template")
            ]
        ]
    )

    await message.reply_photo(
        photo=profile_image,
        caption=caption,
        reply_markup=buttons,
        parse_mode=ParseMode.MARKDOWN
    )


@bot.on_callback_query(filters.regex("^(close_profile|change_template|template_\\d+|back_to_profile)$"))
async def profile_callback_handler(client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id
    total_shiny = await approved_items_collection.count_documents({"user_id": user_id, "type": "shiny"})
    total_legendary = await approved_items_collection.count_documents({"user_id": user_id, "type": "legendary"})
    total_non_legendary = await approved_items_collection.count_documents({"user_id": user_id, "type": "non-legendary"})
    total_tms = 0
    total_teams = 0

    total_approved = total_shiny + total_legendary + total_non_legendary + total_tms + total_teams

    approved_ratio = f"{(total_approved / (total_approved + 0)) * 100:.2f}%" if total_approved > 0 else "0%"

    if data == "close_profile":
        await callback_query.message.delete()

    elif data == "change_template":
        buttons = []
        row = []
        for i in range(1, 16):
            row.append(InlineKeyboardButton(str(i), callback_data=f"template_{i}"))
            if i % 5 == 0:
                buttons.append(row)
                row = []

        if row:
            buttons.append(row)

        buttons.append([InlineKeyboardButton("◀️ Back", callback_data="back_to_profile")])

        await callback_query.message.edit_caption(
            caption="**Select a template for your profile picture:**",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN
        )

    elif data == "back_to_profile":
        selected_template = user_templates.get(user_id, 0)
        profile_image = profile_templates.get(selected_template, default_profile_image)

        # Restore original caption
        caption = f"""(VERIFIED ✅)

★ PROFILE ★
═════════════════════

➤ Name: {callback_query.from_user.first_name or "N/A"}
➤ Username: @{callback_query.from_user.username if callback_query.from_user.username else "N/A"}
➤ User ID: {user_id}

──────────────
Total Approved Items:

➤ Shiny: {total_shiny}
➤ Legendary: {total_legendary}
➤ Non-Legendary: {total_non_legendary}

──────────────
➤ Total Approved : {total_approved}
──────────────
➤ Approved Ratio: {approved_ratio}
──────────────
"""

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Close", callback_data="close_profile"),
                    InlineKeyboardButton("Change Template", callback_data="change_template")
                ]
            ]
        )

        await callback_query.message.edit_media(
            media=InputMediaPhoto(media=profile_image, caption=caption, parse_mode=ParseMode.MARKDOWN),
            reply_markup=buttons
        )

    elif data.startswith("template_"):
        template_num = int(data.split("_")[1])
        user_templates[user_id] = template_num
        image_link = "https://files.catbox.moe/dqt2sw.jpg"

        try:
            await callback_query.message.edit_media(
                media=InputMediaPhoto(media=image_link, caption=callback_query.message.caption, parse_mode=ParseMode.MARKDOWN),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Close", callback_data="close_profile"),
                            InlineKeyboardButton("Change Template", callback_data="change_template")
                        ]
                    ]
                )
            )
        except Exception:
            await callback_query.answer("Failed to change template. Please try again later.", show_alert=True)

@bot.on_message(filters.command("staff"), group=5)
async def staff_command(client, message: Message):
    text = "**God Auction Staff Team**\n\n"
    text += "• Admin: [@God_X_Pawan](https://t.me/God_X_Pawan)\n"
    text += "• Admin: [@Maicra007](https://t.me/Maicra007)\n"
    text += "• Admin: [@One_n_only_1](https://t.me/One_n_only_1)\n"
    text += "• Admin: [@Orewa_cursed](https://t.me/Orewa_cursed)\n"
    await message.reply(text, disable_web_page_preview=True)

@bot.on_message(filters.command("msg") & filters.user(OWNER_IDS), group=5)
async def msg(client, message):
    if len(message.command) < 3:
        return await message.reply("❌ Usage: /msg <user_id> <your message>")

    try:
        user_id = int(message.command[1])
        text = " ".join(message.command[2:])
        await client.send_message(chat_id=user_id, text=f"✉️ Admin Message:\n\n{text}")
        await message.reply("✅ Message sent.")
    except Exception as e:
        await message.reply(f"❌ Failed to send message.\nError: {e}")


@bot.on_message(filters.command("report") & filters.private, group=5)
async def repo(client, message):
    __u__ = message.from_user
    __n__ = __u__.first_name 
    __id__ = __u__.id 

    if len(message.command) < 2:
        return await message.reply_text("❌ Please provide a reason or content for your report.")

    __content__ = " ".join(message.command[1:])

    report = (
        f"🚨 **Report Received** 🚨\n"
        f"👤 Name: {__n__}\n"
        f"🆔 ID: `{__id__}`\n\n"
        f"📝 **Report:**\n> {__content__}\n\n"
        f"📩 *Click below to message the user:*"
    )

    __key__ = InlineKeyboardMarkup([
        [InlineKeyboardButton("MSG 📩", url=f"https://t.me/{client.me.username}?start=msg_{__id__}")]
    ])

    await message.reply_text("✅ Report sent to admins!")

    for owner in OWNER_IDS:
        await client.send_message(chat_id=owner, text=report, reply_markup=__key__, parse_mode="markdown")


@bot.on_message(filters.command(["broadcast", "bcast"]) & filters.user(OWNER_IDS), group=5)
async def broadcast_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: /broadcast Your message here")

    text = message.text.split(None, 1)[1]

    users = await users_collection.find().to_list(length=10000)
    success = 0
    failed = 0

    for user in users:
        try:
            await bot.send_message(chat_id=user["_id"], text=text)
            success += 1
            await asyncio.sleep(0.1)
        except:
            failed += 1

    await message.reply(f"✅ Broadcast sent to {success} users.\n❌ Failed to send to {failed} users.")

@bot.on_message(filters.command("myitems"), group=5)
async def my_items(client, message):
    user_id = message.from_user.id

    items = await approved_items_collection.find({"user_id": user_id}).to_list(length=100)

    if not items:
        return await message.reply("❌ You don't have any approved items in auction.")

    text = f"📦 **Your Auction Items:**\n\n"
    for i, item in enumerate(items, 1):
        msg_id = item.get("auction_id")
        link = f"https://t.me/{AUCTION_CHANNEL_LINK}/{msg_id}"
        text += f"{i}. 🆔 [{item['item_id']}]({link}) | 💰 {item['base_price']} PD\n"

    await message.reply(text, disable_web_page_preview=True)

@bot.on_message(filters.command("mybid"), group=5)
async def my_bid(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    bids = await approved_items_collection.find({"bidder": user_name}).to_list(length=100)

    if not bids:
        return await message.reply("❌ You haven't placed any bids yet.")

    text = f"🧾 **Your Bids, {user_name}:**\n\n"
    for i, bid in enumerate(bids, 1):
        msg_id = bid.get("auction_id")
        link = f"https://t.me/{AUCTION_CHANNEL_LINK}/{msg_id}"
        text += f"{i}. 🆔 [{bid['item_id']}]({link}) | 💰 {bid['base_price']} PD\n"

    await message.reply(text, disable_web_page_preview=True)



user_bid_sessions = {}

@bot.on_message(filters.text & filters.private, group=5)
async def receive_bid_amount(client, message):
    user_id = message.from_user.id

    if user_id in user_bid_sessions:
        try:
            bid_amount = int(message.text)
            item_id = user_bid_sessions[user_id]

            # Auction fetch aur bid logic
            auction = await approved_items_collection.find_one({"item_id": item_id})
            if not auction:
                return await message.reply("❌ Auction not found!")

            current_bid = int(auction.get("base_price", 1000))
            if bid_amount <= current_bid:
                return await message.reply(f"⚠️ Your bid must be higher than {current_bid} PD!")

            previous_bidder_name = auction.get("bidder")
            previous_bidder_id = auction.get("bidder_id")  # Yeh line zaroori hai
            item_name = auction.get("name", "Unknown Item")

            # New bid update
            await approved_items_collection.update_one(
                {"item_id": item_id},
                {"$set": {
                    "base_price": bid_amount,
                    "bidder": message.from_user.first_name,
                    "bidder_id": user_id  # Ab naya bidder bhi save karega
                }}
            )

            # Bid message update
            bid_text = (
                "┏━━━━━━━━━━━━━━━━\n"
                f" 💵 Highest Bid ==> {bid_amount} PD\n"
                f" 👤 By ==> [{message.from_user.first_name}](tg://user?id={user_id})\n"
                "┗━━━━━━━━━━━━━━━━"
            )

            bid_command = f"/start {item_id}"
            encoded_command = quote_plus(bid_command)

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📮 PLACE BID", url=f"https://t.me/God_auction_bot?start={item_id}")]
            ])

            try:
                await client.edit_message_text(
                    chat_id=AUCTION_CHANNEL_ID, message_id=auction["bid_msg_id"], text=bid_text, reply_markup=keyboard
                )
                await message.reply(f"✅ Your bid of {bid_amount} PD has been placed!")

                # Agar previous bidder hai toh usko inform kar
                if previous_bidder_id and previous_bidder_id != user_id:
                    try:
                        bid_again_text = (
                            f"⚡ *Update on your Bid!*\n\n"
                            f"Item: *{item_name}*\n"
                            f"New Highest Bid: `{bid_amount}` PD\n\n"
                            f"[Click here to Bid Again!](https://t.me/God_auction_bot?start={item_id})"
                        )
                        bid_again_button = InlineKeyboardMarkup([
                            [InlineKeyboardButton("📮 PLACE BID", url=f"https://t.me/God_auction_bot?start={item_id}")]
                        ])

                        await client.send_message(
                            chat_id=previous_bidder_id,
                            text=bid_again_text,
                            reply_markup=bid_again_button,
                            parse_mode="Markdown"
                        )
                    except Exception as e:
                        logging.error(f"⚠️ Error sending previous bidder notify: {e}")

            except Exception as e:
                logging.error(f"⚠️ Error updating bid message: {e}")
                await message.reply("⚠️ Failed to update bid message!")

            # Bid complete hone ke baad session delete kar dena
            del user_bid_sessions[user_id]

        except ValueError:
            await message.reply("❌ Please send a valid number for bid amount!")

auction_active = False 
submission_active = False 


@bot.on_message(filters.command("clear"), group=5) 
async def clear_all(client, message):
    owner_id = 7019600964

    if not owner_id:
        return 


    await approved_items_collection.delete_many({}) 
    await message.reply_text(" DONE CLEARATION") 

# **Start Command**
@bot.on_message(filters.command("start"), group=5)
async def start(client, message):
    user_id = int(message.from_user.id) 
    if await users_collection.find_one({"_id": user_id}):
        return  
    await message.reply(
        photo="https://files.catbox.moe/0bs5aq.jpg",
        caption=(
            f"𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗚𝗢𝗗 𝗛𝗲𝘅𝗮 𝗔𝘂𝗰𝘁𝗶𝗼𝗻 𝗕𝗼𝘁🔮 {message.from_user.first_name}\n\n"  
            "◆ 𝗠𝗲𝗴𝗮 𝗕𝗼𝘁 𝗳𝗼𝗿 𝘂𝘀𝗲𝗱 𝘁𝗼 𝗺𝗮𝗻𝗮𝗴𝗲 𝗜𝘁𝗲𝗺𝘀 𝗶𝗻 𝗚𝗢𝗗 𝗛𝗲𝘅𝗮 𝗔𝘂𝗰𝘁𝗶𝗼𝗻 🍁\n\n"  
            "◆ 𝗬𝗼𝘂 𝗰𝗮𝗻 𝗯𝘂𝘆/𝘀𝗲𝗹𝗹 𝗛𝗲𝘅𝗮 𝗜𝘁𝗲𝗺𝘀 𝗨𝘀𝗶𝗻𝗴 𝗧𝗵𝗶𝘀 𝗕𝗼𝘁.\n\n" 
            "◆ Do compulsory  💫\n\n"  
            "◆ Must Join Both Group And Channels 🍁\n"  
            "Link Below 💥\n\n" 
            "Use /add to add Various Hexa Items In auction ✨\n\n" 
            "ɴᴏᴡ, ᴡᴇ ᴀʀᴇ ꜰᴀᴍɪʟʏ💕"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("𝗚𝗥𝗢𝗨𝗣🐉", url="https://t.me/Trainers_union")],
            [InlineKeyboardButton("𝗖𝗛𝗔𝗡𝗡𝗘𝗟🔮", url="https://t.me/God_Auction")]
        ])
                       )

    if message.chat.type != ChatType.PRIVATE:
        await message.reply_text("\"𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 𝙊𝙉𝙇𝙔 𝙄𝙉 𝘿𝙈🔮\"") 
        return 
    await message.reply_photo(
        photo="https://files.catbox.moe/0bs5aq.jpg",
        caption=(
            f"𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗚𝗢𝗗 𝗛𝗲𝘅𝗮 𝗔𝘂𝗰𝘁𝗶𝗼𝗻 𝗕𝗼𝘁🔮 {message.from_user.first_name}\n\n"  
            "◆ 𝗠𝗲𝗴𝗮 𝗕𝗼𝘁 𝗳𝗼𝗿 𝘂𝘀𝗲𝗱 𝘁𝗼 𝗺𝗮𝗻𝗮𝗴𝗲 𝗜𝘁𝗲𝗺𝘀 𝗶𝗻 𝗚𝗢𝗗 𝗛𝗲𝘅𝗮 𝗔𝘂𝗰𝘁𝗶𝗼𝗻 🍁\n\n"  
            "◆ 𝗬𝗼𝘂 𝗰𝗮𝗻 𝗯𝘂𝘆/𝘀𝗲𝗹𝗹 𝗛𝗲𝘅𝗮 𝗜𝘁𝗲𝗺𝘀 𝗨𝘀𝗶𝗻𝗴 𝗧𝗵𝗶𝘀 𝗕𝗼𝘁.\n\n" 
            "◆ Do compulsory  💫\n\n"  
            "◆ Must Join Both Group And Channels 🍁\n"  
            "Link Below 💥\n\n" 
            "Use /add to add Various Hexa Items In auction ✨\n\n" 
            "ɴᴏᴡ, ᴡᴇ ᴀʀᴇ ꜰᴀᴍɪʟʏ💕"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("𝗚𝗥𝗢𝗨𝗣🐉", url="https://t.me/Trainers_union")],
            [InlineKeyboardButton("𝗖𝗛𝗔𝗡𝗡𝗘𝗟🔮", url="https://t.me/God_Auction")]
        ])
    )

    await users_collection.insert_one({"_id": user_id}) 


@bot.on_message(filters.command("rules"), group=5)
async def rules(client, message):
    """Sends the auction rules."""
    await message.reply_text(
        "<blockquote>★ God Auction Bid Rules\n\n"
        "• 20% Of bid amount will be taken as fine for removing bid\n"
        "• 10% if bid was over 100k\n"
        "• Under 3 hours you will have to /report for removing your bids else after 3 hours direct ban or 10k Fine.\n\n"
        "★ God Auction Submission Rules\n\n"
        "• 80% Of highest bid amount PD will be taken as fine for removing your approved pokes from the auction\n"
        "• Your items can be cancelled for free if you report when your item is pending.\n"
        "• Under 5 hours you will have to /report for removing your approved item else after 5 hours direct ban or 20k Fine.\n\n"
        "For Any Queries 📞 Contact With our Staff by Command (/staff) or (/report)</blockquote>", 
        parse_mode=ParseMode.HTML
    )


@bot.on_message(filters.command("start_auction") & filters.user(OWNER_IDS), group=5)
async def start_auction(client, message):
    global auction_active
    if auction_active:
        return await message.reply("⚠️ **Auction is already active!**")

    auction_active = True
    await message.reply("✅ **Auction has started!** Now you can bid and submit Pokémon.")

@bot.on_message(filters.command("end_auction") & filters.user(OWNER_IDS), group=5)
async def end_auction(client, message):
    global auction_active
    if not auction_active:
        return await message.reply("⚠️ **No active auction to end!**")

    auction_active = False
    await message.reply("❌ **Auction has ended!** No further bids or submissions allowed.")

@bot.on_message(filters.command("start_submission") & filters.user(OWNER_IDS), group=5)
async def start_submission(client, message):
    global submission_active
    if submission_active:
        return await message.reply("⚠️ **Submission is already active!**")

    submission_active = True
    await message.reply("✅ **Pokémon submission is now open!** Use `/add` to submit.")

@bot.on_message(filters.command("end_submission") & filters.user(OWNER_IDS), group=5)
async def end_submission(client, message):
    global submission_active
    if not submission_active:
        return await message.reply("⚠️ **No active submission process to end!**")

    submission_active = False
    await message.reply("❌ **Submission is now closed!** No further Pokémon can be submitted.")


@bot.on_message(filters.command("items"), group=5)
async def list_items(client, message):
    """Lists all approved Pokémon categorized properly."""
    approved_items = await approved_items_collection.find().to_list(length=None)

    categories = {
        "⭐ Legendary Pokémon": [],
        "🔹 Non-Legendary Pokémon": [],
        "✨ Shiny Pokémon": [],
        "💳 Tms": []
    }

    for item in approved_items:
        category = item.get("type")
        name = item.get('tms_info') and item.get("name") 
        msg_id = item.get("auction_id")
        link = f"https://{AUCTION_CHANNEL_LINK}/{msg_id}"

        if category == "legendary":
            categories["⭐ Legendary Pokémon"].append(f"🔸 [{name}]({link})")
        elif category == "nonlegendary":
            categories["🔹 Non-Legendary Pokémon"].append(f"🔹 [{name}]({link})")
        elif category == "shiny":
            categories["✨ Shiny Pokémon"].append(f"✨ [{name}]({link})")
        elif category == "tms":
            categories["💳 TMs"].append(f"💳 [{name}]({link})")

    # ✅ **Format and Send the Message**
    items_text = "**📜 Approved Pokémon in Auction**\n\n"
    for category, items in categories.items():
        if items:
            items_text += f"**{category}:**\n" + "\n".join(items) + "\n\n"

    if not any(categories.values()):
        items_text += "❌ No approved Pokémon available for bidding yet."

    await message.reply_text(items_text,  disable_web_page_preview=True)

# **Safe Message Sending**
async def send_message_safe(client, chat_id, text, reply_markup=None):
    try:
        await client.send_message(chat_id, text, reply_markup=reply_markup)
    except Exception as e:
        logging.error(f"Failed to send message to {chat_id}: {e}")