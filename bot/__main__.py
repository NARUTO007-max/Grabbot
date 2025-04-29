from bot.db import (users_collection)
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, CallbackContext
import logging

# Bot Token
API_TOKEN = '7608107574:AAGMrCB5b3O5vJJNvu07cQ8vsmkzRksjN74'  # Replace with your bot token

# Admin ID
YOUR_ADMIN_ID = 7019600964  # Replace with your admin ID

# Group/channel link
GROUP_LINK = "https://t.me/animaction_world_in_2025"  # Apna group link daal

# Owner username
OWNER_USERNAME = "Uzumaki_X_Naruto_6"  # Apna username daal (without @)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Pehle database me save karo
    if not users_collection.find_one({"user_id": user.id}):
        users_collection.insert_one({
            "user_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
        })

    keyboard = [
        [
            InlineKeyboardButton("⚡ ᎧᏇᏁᏒ ⚡", url=f"https://t.me/{OWNER_USERNAME}"),
            InlineKeyboardButton("⚡ ᎶᏒᎧᏬᎮ ⚡", url=GROUP_LINK)
        ],
        [
            InlineKeyboardButton("⚡ ᏨᏝᎧᏕᏋ ⚡", callback_data="close")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Yeh line add karo:
    name = user.first_name  # <-- yeh compulsory hai caption ke liye

    # Photo and caption
    photo_url = "https://files.catbox.moe/461mqe.jpg"
    caption = f"""✨ Welcome {name} to HinataX Support Bot!

Your ultimate assistant for managing and protecting your group.

⚡ Features:
• Auto-Moderation & Filters
• Welcome & Goodbye Messages
• Anti-Spam & Flood Control
• Warn, Mute, Ban, Kick Commands
• Fun and Utility Commands
• 24/7 Active Support

✨ Empower your group with smart management and peace of mind!

🔹 Use /help to explore all commands.
🔹 For support, contact: @Uzumaki_X_Naruto_6
"""

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=caption,
        reply_markup=reply_markup
    )

# Button click handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "close":
        try:
            await query.message.delete()
        except Exception as e:
            logger.error(f"Error deleting message: {e}")

# Left chat member handler
async def user_left(update: Update, context: CallbackContext):
    if update.message.left_chat_member:
        user = update.message.left_chat_member
        user_name = user.first_name if user.first_name else "Unknown"
        user_id = user.id
        user_username = f"@{user.username}" if user.username else "No Username"

        # Group members count
        chat = await context.bot.get_chat(update.message.chat_id)
        members_count = await chat.get_member_count()

        # User profile pic
        try:
            photos = await context.bot.get_user_profile_photos(user_id)
            if photos.total_count > 0:
                file_id = photos.photos[0][-1].file_id
            else:
                file_id = None
        except:
            file_id = None

        # Caption
        caption = f"""⎊─────☵ ɢᴏᴏᴅʙʏᴇ ☵─────⎊

▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬

☉ ɴᴀᴍᴇ ⧽ {user_name}
☉ ɪᴅ ⧽ {user_id}
☉ ᴜ_ɴᴀᴍᴇ ⧽ {user_username}
☉ ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs ⧽ {members_count}

▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬

⎉──────▢✭ 侖 ✭▢──────⎉"""

        if file_id:
            await update.message.reply_photo(photo=file_id, caption=caption)
        else:
            await update.message.reply_text(caption)

# New member joined handler
async def user_joined(update: Update, context: CallbackContext):
    if update.message.new_chat_members:
        for user in update.message.new_chat_members:
            user_name = user.first_name if user.first_name else "Unknown"
            user_id = user.id
            user_username = f"@{user.username}" if user.username else "No Username"

            # Group members count
            chat = await context.bot.get_chat(update.message.chat_id)
            members_count = await chat.get_member_count()

            # User profile pic
            try:
                photos = await context.bot.get_user_profile_photos(user_id)
                if photos.total_count > 0:
                    file_id = photos.photos[0][-1].file_id
                else:
                    file_id = None
            except:
                file_id = None

            # Caption
            caption = f"""⎊─────☵ ᴡᴇʟᴄᴏᴍᴇ ☵─────⎊

▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬

☉ ɴᴀᴍᴇ ⧽ {user_name}
☉ ɪᴅ ⧽ {user_id}
☉ ᴜ_ɴᴀᴍᴇ ⧽ {user_username}
☉ ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs ⧽ {members_count}

▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬

⎉──────▢✭ 侖 ✭▢──────⎉"""

            if file_id:
                await update.message.reply_photo(photo=file_id, caption=caption)
            else:
                await update.message.reply_text(caption)

# /ban command
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type not in ['group', 'supergroup']:
        await update.message.reply_text("⚠️ This command can only be used in groups.")
        return

    bot_member = await context.bot.get_chat_member(update.message.chat.id, context.bot.id)
    if not bot_member.can_restrict_members:
        await update.message.reply_text("⚠️ I don't have permission to ban members!")
        return

    user_id = None
    username = None

    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        user_id = user.id
        username = user.mention_html()
    elif context.args:
        user_id = int(context.args[0])
        try:
            user = await context.bot.get_chat_member(update.message.chat.id, user_id)
            username = user.user.mention_html()
        except:
            username = f"user with ID {user_id}"

    if not user_id:
        await update.message.reply_text("⚠️ Please reply to a user's message or provide a user ID to ban.")
        return

    try:
        await context.bot.ban_chat_member(chat_id=update.message.chat.id, user_id=user_id)
        await update.message.reply_html(f"🚫 Banned {username} successfully!")
    except Exception as e:
        await update.message.reply_text(f"❌ An error occurred while banning:\n{e}")

# /unban command
async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type not in ['group', 'supergroup']:
        await update.message.reply_text("⚠️ This command can only be used in groups.")
        return

    bot_member = await context.bot.get_chat_member(update.message.chat.id, context.bot.id)
    if not bot_member.can_restrict_members:
        await update.message.reply_text("⚠️ I don't have permission to unban members!")
        return

    user_id = None
    username = None

    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        user_id = user.id
        username = user.mention_html()
    elif context.args:
        user_id = int(context.args[0])
        try:
            user = await context.bot.get_chat_member(update.message.chat.id, user_id)
            username = user.user.mention_html()
        except:
            username = f"user with ID {user_id}"

    if not user_id:
        await update.message.reply_text("⚠️ Please reply to a user's message or provide a user ID to unban.")
        return

    try:
        await context.bot.unban_chat_member(chat_id=update.message.chat.id, user_id=user_id)
        await update.message.reply_html(f"✅ Unbanned {username} successfully!")
    except Exception as e:
        await update.message.reply_text(f"❌ An error occurred while unbanning:\n{e}")

async def promote_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        user_id = user.id
    elif context.args:
        user_id = int(context.args[0])
        user = await context.bot.get_chat_member(update.effective_chat.id, user_id).user
    else:
        await update.message.reply_text("Please reply to a user or provide a user ID to promote.")
        return

    try:
        await context.bot.promote_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            can_change_info=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=False,
            can_manage_video_chats=True,
            can_manage_chat=True
        )
        await update.message.reply_text(f"Successfully promoted @{user.username} ✅")
    except Exception as e:
        await update.message.reply_text(f"An error occurred while promoting the user: {e}")

async def demote_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        user_id = user.id
    elif context.args:
        user_id = int(context.args[0])
        user = await context.bot.get_chat_member(update.effective_chat.id, user_id).user
    else:
        await update.message.reply_text("Please reply to a user or provide a user ID to demote.")
        return

    try:
        await context.bot.promote_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            can_change_info=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_video_chats=False,
            can_manage_chat=False
        )
        await update.message.reply_text(f"Successfully demoted @{user.username} ✅")
    except Exception as e:
        await update.message.reply_text(f"An error occurred while demoting the user: {e}")

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    reply_user = update.message.reply_to_message.from_user if update.message.reply_to_message else None

    text = f"**Your ID:** `{user.id}`\n**Chat ID:** `{chat.id}`"

    if reply_user:
        text += f"\n**Replied User ID:** `{reply_user.id}`"

    await update.message.reply_text(text, parse_mode="Markdown")

# /broadcast command for admin
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_ids = [7019600964]  # <-- Apna admin ID daal
    user_id = update.effective_user.id

    if user_id not in admin_ids:
        await update.message.reply_text("Sorry, you are not authorized to use this command.")
        return

    if not context.args:
        await update.message.reply_text("Please provide a message to broadcast.")
        return

    broadcast_message = " ".join(context.args)

    # Fetch all user IDs from MongoDB
    users = users_collection.find()
    all_user_ids = [user["user_id"] for user in users]

    for user_id in all_user_ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=broadcast_message)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

    await update.message.reply_text("Broadcast message sent to all users.")

# Main function
def main():
    application = Application.builder().token(API_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, user_left))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, user_joined))
    application.add_handler(CommandHandler("ban", ban_user))
    application.add_handler(CommandHandler("unban", unban_user))
    application.add_handler(CommandHandler("promote", promote_user))
    application.add_handler(CommandHandler("demote", demote_user))
    application.add_handler(CommandHandler("id", id_command))  
    application.add_handler(CommandHandler("broadcast", broadcast))  # <- Ye line sahi jagah aayi, same level par

    # Run
    application.run_polling()

if __name__ == '__main__':
    main()