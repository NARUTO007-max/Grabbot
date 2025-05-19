import os
import random
import asyncio
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageChops
from pyrogram import Client, filters, enums
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton, Message
from typing import Union, Optional
from logging import getLogger
from datetime import datetime, timedelta, timezone
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant

# --- Your Bot Credentials ---
app = Client(
    "utag_bot",
    api_id=25698862,
    api_hash="7d7739b44f5f8c825d48cc6787889dbc",
    bot_token="7982886378:AAEcf-VbY9bvj-4DFMLe4rMOQMlJpD8TfGY"
)

# --- Admin Filter ---
async def is_admin(_, __, message):
    try:
        member = await message.chat.get_member(message.from_user.id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
        return False

admin_filter = filters.create(is_admin)

# --- Tag All Users Command ---
spam_chats = []

@app.on_message(filters.command(["utag", "all", "mention"]) & filters.group & admin_filter)
async def tag_all_users(_, message): 
    replied = message.reply_to_message  
    if len(message.command) < 2 and not replied:
        return await message.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴛᴀɢ ᴀʟʟ**") 

    spam_chats.append(message.chat.id)      
    usernum = 0
    usertxt = ""
    if replied:
        async for m in app.get_chat_members(message.chat.id): 
            if message.chat.id not in spam_chats:
                break       
            usernum += 5
            usertxt += f"\n⊚ [{m.user.first_name}](tg://user?id={m.user.id})\n"
            if usernum == 1:
                await replied.reply_text(usertxt)
                await asyncio.sleep(3)
                usernum = 0
                usertxt = ""
    else:
        text = message.text.split(None, 1)[1]
        async for m in app.get_chat_members(message.chat.id):       
            if message.chat.id not in spam_chats:
                break 
            usernum += 1
            usertxt += f"\n⊚ [{m.user.first_name}](tg://user?id={m.user.id})\n"
            if usernum == 5:
                await app.send_message(message.chat.id, f'{text}\n{usertxt}')
                await asyncio.sleep(3)
                usernum = 0
                usertxt = ""

    try:
        spam_chats.remove(message.chat.id)
    except:
        pass        

# --- Cancel Command ---
@app.on_message(filters.command(["cancel", "ustop"]))
async def cancel_spam(client, message):
    if message.chat.id not in spam_chats:
        return await message.reply("𝐂𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲 𝐈'𝐦 𝐍𝐨𝐭 ..")

    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
        if participant.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            return await message.reply("𝐘𝐨𝐮 𝐀𝐫𝐞 𝐍𝐨𝐭 𝐀𝐝𝐦𝐢𝐧 𝐁𝐚𝐛𝐲")
    except:
        return await message.reply("𝐂𝐨𝐮𝐥𝐝 𝐍𝐨𝐭 𝐕𝐞𝐫𝐢𝐟𝐲 𝐘𝐨𝐮𝐫 𝐒𝐭𝐚𝐭𝐮𝐬")

    try:
        spam_chats.remove(message.chat.id)
    except:
        pass
    return await message.reply("**🦋ᴛᴀɢ ʀᴏᴋɴᴇ ᴡᴀʟᴇ ᴋɪ ᴍᴀᴀ ᴋᴀ ʙʜᴀʀᴏsᴀ Naruto.....🫠**")

LOGGER = getLogger(__name__)


class WelDatabase:
    def __init__(self):
        self.data = {}
        self.join_counts = {}
        self.join_timestamps = {}
        self.auto_disabled = {}

    async def find_one(self, chat_id):
        return self.data.get(chat_id, {"state": "on"})

    async def set_state(self, chat_id, state):
        self.data[chat_id] = {"state": state}

    async def is_welcome_on(self, chat_id):
        chat_data = await self.find_one(chat_id)
        return chat_data.get("state") == "on"

    async def track_join(self, chat_id):
        now = datetime.now(timezone.utc)
        last_join_time = self.join_timestamps.get(chat_id, now)
        if (now - last_join_time).total_seconds() > 8:
            self.join_counts[chat_id] = 1
        else:
            self.join_counts[chat_id] = self.join_counts.get(chat_id, 0) + 1
        self.join_timestamps[chat_id] = now
        return self.join_counts[chat_id]

    async def auto_disable_welcome(self, chat_id):
        await self.set_state(chat_id, "off")
        self.auto_disabled[chat_id] = datetime.now(timezone.utc) + timedelta(minutes=30)

    async def check_auto_reenable(self, chat_id):
        disable_time = self.auto_disabled.get(chat_id)
        if disable_time and datetime.now(timezone.utc) >= disable_time:
            await self.set_state(chat_id, "on")
            del self.auto_disabled[chat_id]
            return True
        return False

wlcm = WelDatabase()

class temp:
    MELCOW = {}

def circle(pfp, size=(500, 500)):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS)
    pfp.putalpha(mask)
    return pfp


def welcomepic(pic_path, user, chatname, user_id, uname):
    background = Image.open("ANNIEMUSIC/assets/annie/AnnieNwel.png")
    pfp = Image.open(pic_path).convert("RGBA")
    pfp = circle(pfp, size=(835, 839))
    draw = ImageDraw.Draw(background)
    font_large = ImageFont.truetype('ANNIEMUSIC/assets/annie/ArialReg.ttf', size=65)
    draw.text((421, 715), f'{user}', fill=(242, 242, 242), font=font_large)
    draw.text((270, 1005), f'{user_id}', fill=(242, 242, 242), font=font_large)
    draw.text((570, 1308), f"{uname}", fill=(242, 242, 242), font=font_large)
    pfp_position = (1887, 390)
    background.paste(pfp, pfp_position, pfp)
    image_path = f"downloads/welcome#{user_id}.png"
    background.save(image_path)
    return image_path


@app.on_message(filters.command("wel") & ~filters.private)
async def auto_state(client, message):
    usage = "**Usage:**\n⦿/wel [on|off]\n➤ANNIE SPECIAL WELCOME.........."
    if len(message.command) != 2:
        return await message.reply_text(usage)

    chat_id = message.chat.id
    user_status = await client.get_chat_member(chat_id, message.from_user.id)
    if user_status.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await message.reply_text("**sᴏʀʀʏ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴄʜᴀɴɢᴇ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ sᴛᴀᴛᴜs!**")

    state = message.text.split(None, 1)[1].strip().lower()
    current_state = await wlcm.find_one(chat_id)
    if state == "off":
        if current_state.get("state") == "off":
            await message.reply_text("**ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ!**")
        else:
            await wlcm.set_state(chat_id, "off")
            await message.reply_text(f"**ᴅɪsᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ɪɴ {message.chat.title}**")
    elif state == "on":
        if current_state.get("state") == "on":
            await message.reply_text("**ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ!**")
        else:
            await wlcm.set_state(chat_id, "on")
            await message.reply_text(f"**ᴇɴᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ɪɴ {message.chat.title}**")
    else:
        await message.reply_text(usage)


@app.on_chat_member_updated(filters.group, group=-3)
async def greet_new_member(client, member: ChatMemberUpdated):
    chat_id = member.chat.id
    user = member.new_chat_member.user if member.new_chat_member else member.from_user

    welcome_enabled = await wlcm.is_welcome_on(chat_id)
    if not welcome_enabled:
        auto_reenabled = await wlcm.check_auto_reenable(chat_id)
        if auto_reenabled:
            await client.send_message(
                chat_id,
                "**ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇs ʜᴀᴠᴇ ʙᴇᴇɴ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʀᴇ-ᴇɴᴀʙʟᴇᴅ.**"
            )
        else:
            return

    join_count = await wlcm.track_join(chat_id)
    if join_count >= 10:
        await wlcm.auto_disable_welcome(chat_id)
        await client.send_message(
            chat_id,
            "**ᴍᴀssɪᴠᴇ ᴊᴏɪɴ ᴅᴇᴛᴇᴄᴛᴇᴅ. ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇs ᴀʀᴇ ᴛᴇᴍᴘᴏʀᴀʀɪʟʏ ᴅɪsᴀʙʟᴇᴅ ғᴏʀ 30 ᴍɪɴᴜᴛᴇs.**"
        )
        return

    if member.new_chat_member and member.new_chat_member.status == enums.ChatMemberStatus.MEMBER:
        try:
            pic_path = None
            if user.photo:
                pic_path = await client.download_media(
                    user.photo.big_file_id, file_name=f"downloads/pp{user.id}.png"
                )
            else:
                pic_path = "ANNIEMUSIC/assets/upic.png"

            previous_message = temp.MELCOW.get(f"welcome-{chat_id}")
            if previous_message:
                try:
                    await previous_message.delete()
                except Exception as e:
                    LOGGER.error(f"Error deleting previous welcome message: {e}")

            welcome_img = welcomepic(
                pic_path, user.first_name, member.chat.title, user.id, user.username or "No Username"
            )

            count = await client.get_chat_members_count(chat_id)
            button_text = "๏ ᴠɪᴇᴡ ɴᴇᴡ ᴍᴇᴍʙᴇʀ ๏"
            add_button_text = "๏ ᴋɪᴅɴᴀᴘ ᴍᴇ ๏"
            deep_link = f"tg://openmessage?user_id={user.id}"
            add_link = f"https://t.me/{client.username}?startgroup=true"
            welcome_message = await client.send_photo(
                chat_id,
                photo=welcome_img,
                caption=f"""
**❅────✦ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ✦────❅
{member.chat.title}
▰▰▰▰▰▰▰▰▰▰▰▰▰
➻ Nᴀᴍᴇ ✧ {user.mention}
➻ Iᴅ ✧ `{user.id}`
➻ Usᴇʀɴᴀᴍᴇ ✧ @{user.username or "No Username"}
➻ Tᴏᴛᴀʟ Mᴇᴍʙᴇʀs ✧ {count}
▰▰▰▰▰▰▰▰▰▰▰▰▰**
**❅─────✧❅✦❅✧─────❅**
""",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(button_text, url=deep_link)],
                    [InlineKeyboardButton(add_button_text, url=add_link)],
                ])
            )
            temp.MELCOW[f"welcome-{chat_id}"] = welcome_message

            if pic_path and os.path.exists(pic_path) and "ANNIEMUSIC/assets/upic.png" not in pic_path:
                os.remove(pic_path)
            if welcome_img and os.path.exists(welcome_img):
                os.remove(welcome_img)

        except Exception as e:
            LOGGER.error(f"Error in greeting new member: {e}")

# --- Run Bot ---
app.run()