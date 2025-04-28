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
    keyboard = [
        [
            InlineKeyboardButton("👑 Owner", url=f"https://t.me/{OWNER_USERNAME}"),
            InlineKeyboardButton("🌐 Group", url=GROUP_LINK)
        ],
        [
            InlineKeyboardButton("❌ Close", callback_data="close")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Photo and caption
    photo_url = "https://files.catbox.moe/62uskb.jpg"  # Koi bhi welcome image ka link daal
    caption = f"✨ Welcome to the bot!\n\n👑 Owner: @{OWNER_USERNAME}\n🌐 Join our group!"

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
        await update.message.reply_text("This command can only be used in groups.")
        return

    bot_member = await context.bot.get_chat_member(update.message.chat_id, context.bot.id)
    if not bot_member.can_restrict_members:
        await update.message.reply_text("I don't have permission to ban members!")
        return

    user_id = None

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    elif context.args:
        user_id = int(context.args[0])

    if not user_id:
        await update.message.reply_text("Please reply to a user's message or provide a user ID to ban.")
        return

    try:
        await context.bot.ban_chat_member(chat_id=update.message.chat_id, user_id=user_id)
        await update.message.reply_text(f"Another one bites the dust...!
Banned {username}.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred while banning: {e}")

# /unban command
async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type not in ['group', 'supergroup']:
        await update.message.reply_text("This command can only be used in groups.")
        return

    bot_member = await context.bot.get_chat_member(update.message.chat_id, context.bot.id)
    if not bot_member.can_restrict_members:
        await update.message.reply_text("I don't have permission to unban members!")
        return

    user_id = None

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    elif context.args:
        user_id = int(context.args[0])

    if not user_id:
        await update.message.reply_text("Please reply to a user's message or provide a user ID to unban.")
        return

    try:
        await context.bot.unban_chat_member(chat_id=update.message.chat_id, user_id=user_id)
        await update.message.reply_text(f"Fine, they can join again.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred while unbanning: {e}")

# Main function
def main():
    application = Application.builder().token(API_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, user_left))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, user_joined))  # New user handler
    application.add_handler(CommandHandler("ban", ban_user))
    application.add_handler(CommandHandler("unban", unban_user))

    # Run
    application.run_polling()
if __name__ == '__main__':
    main()