from bot.db import users_collection
from telegram import ChatPermissions
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext,
)
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

# Broadcast Command (for Owner only)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user is OWNER
    OWNER_IDS = [7019600964]  # <-- Apne OWNER ID yaha daalna
    if update.effective_user.id not in OWNER_IDS:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    # Check if message has text to broadcast
    if not context.args:
        await update.message.reply_text("❌ Usage: /broadcast Your message here")
        return

    text = " ".join(context.args)

    # Ab users database se fetch karna hai (assume karte hain users ko kahi store kiya hai)
    users = []  # TODO: Apna database se users list yaha laana
    # Example: users = await users_collection.find().to_list(length=10000)

    success = 0
    failed = 0

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=text)
            success += 1
            await asyncio.sleep(0.1)
        except:
            failed += 1

    await update.message.reply_text(f"✅ Broadcast sent to {success} users.\n❌ Failed to send to {failed} users.")

# Group tagging control
group_tagging = {}

# /all command
async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    sender = update.effective_user

    # Check if used in group
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("This command only works in groups!")
        return

    # Check if sender is an admin
    member = await chat.get_member(sender.id)
    if member.status not in ["administrator", "creator"]:
        await update.message.reply_text("Only admins are allowed to use this command.")
        return

    # Enable tagging for the group
    group_tagging[chat.id] = True

    # WARNING: Telegram API limitation => Bots can't fetch all group members normally.
    # Workaround: We'll tag only recent chat members (those active recently)

    # Fetch administrators (optional if you want to exclude only bots)
    admins = await chat.get_administrators()
    admin_ids = [admin.user.id for admin in admins]

    # Prepare mention text
    mention_text = ""

    try:
        async for member in context.bot.get_chat_members(chat.id):
            if member.user.is_bot:
                continue
            if member.user.id in admin_ids:
                continue  # Skip admins if you don't want to tag them
            if member.user.username:
                mention_text += f"⊚ @{member.user.username}\n"
            else:
                mention_text += f"⊚ {member.user.first_name}\n"
    except Exception as e:
        # Bot can't fetch all users (Telegram limits), so fallback:
        await update.message.reply_text("Bot cannot fetch all group members (API limit). Tagging only admins!")
        for admin in admins:
            if admin.user.is_bot:
                continue
            if admin.user.username:
                mention_text += f"⊚ @{admin.user.username}\n"
            else:
                mention_text += f"⊚ {admin.user.first_name}\n"

    if not mention_text:
        await update.message.reply_text("No members found to tag.")
        return

    # Combine with original message text
    original_text = update.message.text.replace('/all', '').replace('@all', '').strip()
    final_text = f"{original_text}\n\n{mention_text}"

    # Send message (split if necessary)
    if len(final_text) <= 4096:
        await update.message.reply_text(final_text)
    else:
        for i in range(0, len(final_text), 4000):
            await update.message.reply_text(final_text[i:i+4000])

# /alloff command
async def stop_tagging(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    sender = update.effective_user

    # Check if used in group
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("This command only works in groups!")
        return

    # Check if sender is an admin
    member = await chat.get_member(sender.id)
    if member.status not in ["administrator", "creator"]:
        await update.message.reply_text("Only admins are allowed to use this command.")
        return

    # Disable tagging
    group_tagging[chat.id] = False
    await update.message.reply_text("➥ Tagging turned off by /alloff")

# Warning system memory
user_warnings = {}

# /warn command
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    sender = update.effective_user

    # Check if used in group
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("This command only works in groups!")
        return

    # Check if sender is an admin
    member = await chat.get_member(sender.id)
    if member.status not in ["administrator", "creator"]:
        await update.message.reply_text("Only admins are allowed to issue warnings.")
        return

    # Check if user to warn is mentioned
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user's message to warn them.")
        return

    warned_user = update.message.reply_to_message.from_user
    user_id = warned_user.id

    # Increase warning count
    user_warnings.setdefault(chat.id, {})
    user_warnings[chat.id][user_id] = user_warnings[chat.id].get(user_id, 0) + 1

    warnings = user_warnings[chat.id][user_id]
    if warnings >= 3:
        await update.message.reply_text(f"⚠️ User {warned_user.first_name} has {warnings}/3 warnings! ⚠️\nAction needed!")
        # You can add automatic ban/kick here if needed
    else:
        await update.message.reply_text(f"User {warned_user.first_name} has {warnings}/3 warnings; be careful!")

# /unwarn command
async def unwarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    sender = update.effective_user

    # Check if used in group
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("This command only works in groups!")
        return

    # Check if sender is an admin
    member = await chat.get_member(sender.id)
    if member.status not in ["administrator", "creator"]:
        await update.message.reply_text("Only admins are allowed to remove warnings.")
        return

    # Check if user to unwarn is mentioned
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user's message to remove their warning.")
        return

    warned_user = update.message.reply_to_message.from_user
    user_id = warned_user.id

    # Remove warning
    if chat.id in user_warnings and user_id in user_warnings[chat.id]:
        if user_warnings[chat.id][user_id] > 0:
            user_warnings[chat.id][user_id] -= 1
            warnings = user_warnings[chat.id][user_id]
            await update.message.reply_text(f"Warning removed for {warned_user.first_name} (now {warnings}/3 warnings)")
        else:
            await update.message.reply_text(f"{warned_user.first_name} has no warnings.")
    else:
        await update.message.reply_text(f"{warned_user.first_name} has no warnings.")

# /mute command
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    sender = update.effective_user

    # Only groups
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("This command only works in groups!")
        return

    # Only admins can mute
    sender_member = await chat.get_member(sender.id)
    if sender_member.status not in ["administrator", "creator"]:
        await update.message.reply_text("Only admins can mute users.")
        return

    # Target user
    user_to_mute = None
    if update.message.reply_to_message:
        user_to_mute = update.message.reply_to_message.from_user
    elif context.args:
        username = context.args[0]
        if username.startswith('@'):
            username = username[1:]
        try:
            user_info = await context.bot.get_chat_member(chat.id, username)
            user_to_mute = user_info.user
        except Exception:
            await update.message.reply_text("Couldn't find the user. Please reply or mention username!")
            return
    else:
        await update.message.reply_text("Reply to a user or provide a username to mute.")
        return

    # Check if target is admin
    target_member = await chat.get_member(user_to_mute.id)
    if target_member.status in ["administrator", "creator"]:
        await update.message.reply_text("You cannot mute an admin!")
        return

    # Mute (permanent)
    await context.bot.restrict_chat_member(
        chat.id,
        user_to_mute.id,
        permissions=ChatPermissions(can_send_messages=False)
    )

    await update.message.reply_text(f"🔇 Muted {user_to_mute.mention_html()} successfully!", parse_mode="HTML")

# /unmute command
async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    sender = update.effective_user

    # Only groups
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("This command only works in groups!")
        return

    # Only admins can unmute
    sender_member = await chat.get_member(sender.id)
    if sender_member.status not in ["administrator", "creator"]:
        await update.message.reply_text("Only admins can unmute users.")
        return

    # Target user
    user_to_unmute = None
    if update.message.reply_to_message:
        user_to_unmute = update.message.reply_to_message.from_user
    elif context.args:
        username = context.args[0]
        if username.startswith('@'):
            username = username[1:]
        try:
            user_info = await context.bot.get_chat_member(chat.id, username)
            user_to_unmute = user_info.user
        except Exception:
            await update.message.reply_text("Couldn't find the user. Please reply or mention username!")
            return
    else:
        await update.message.reply_text("Reply to a user or provide a username to unmute.")
        return

    # Unmute
    await context.bot.restrict_chat_member(
        chat.id,
        user_to_unmute.id,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )
    )

    await update.message.reply_text(f"🔊 Unmuted {user_to_unmute.mention_html()} successfully!", parse_mode="HTML")

# /kick command
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    sender = update.effective_user

    # Check if used in group
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("This command only works in groups!")
        return

    member = await chat.get_member(sender.id)

    # If normal member => kick themselves
    if member.status not in ["administrator", "creator"]:
        try:
            await context.bot.ban_chat_member(chat_id=chat.id, user_id=sender.id)
            await context.bot.unban_chat_member(chat_id=chat.id, user_id=sender.id)  # Unban for rejoin
        except Exception as e:
            await update.message.reply_text("Unable to kick you.")
        return

    # Admin usage
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a user's message to kick them.")
        return

    target_user = update.message.reply_to_message.from_user

    if target_user.id == sender.id:
        await update.message.reply_text("You cannot kick yourself like this, just use /kick alone.")
        return

    # Prepare Confirm/Cancel buttons
    keyboard = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_kick:{target_user.id}"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_kick")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"⚡ Admin {sender.mention_html()} wants to kick {target_user.mention_html()}.\nAre you sure?",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

# Callback Query Handler
async def kick_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "cancel_kick":
        await query.edit_message_text("❌ Kick cancelled.")
        return

    if data.startswith("confirm_kick:"):
        user_id = int(data.split(":")[1])
        chat = update.effective_chat
        try:
            await context.bot.ban_chat_member(chat_id=chat.id, user_id=user_id)
            await context.bot.unban_chat_member(chat_id=chat.id, user_id=user_id)
            await query.edit_message_text("✅ User kicked successfully!")
        except Exception as e:
            await query.edit_message_text("Failed to kick the user.")

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
    application.add_handler(CommandHandler("broadcast", broadcast))  
    application.add_handler(CommandHandler(["all", "tagall"], tag_all))
    application.add_handler(CommandHandler("alloff", stop_tagging))

    # Warn/unwarn handlers
    application.add_handler(CommandHandler("warn", warn))
    application.add_handler(CommandHandler("unwarn", unwarn))

    # Mute/unmute handlers
    application.add_handler(CommandHandler("mute", mute_user))
    application.add_handler(CommandHandler("unmute", unmute_user))

    # Kick handlers
    application.add_handler(CommandHandler("kick", kick))
    application.add_handler(CallbackQueryHandler(kick_buttons, pattern="^(confirm_kick|cancel_kick)"))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()