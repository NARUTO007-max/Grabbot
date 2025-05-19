import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant

# --- Your Bot Credentials ---
app = Client(
    "utag_bot",
    api_id=25698862,
    api_hash="7d7739b44f5f8c825d48cc6787889dbc",
    bot_token="7608107574:AAH_PGTsl7ua9IY9C1GQOz5qdU8XjXATH80"
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

# --- Run Bot ---
app.run()