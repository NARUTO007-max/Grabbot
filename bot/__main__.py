from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import bot.db as db

API_TOKEN = "7608107574:AAGMrCB5b3O5vJJNvu07cQ8vsmkzRksjN74"
WELCOME_IMAGE = "https://files.catbox.moe/9eehwa.jpg"

# Add your Telegram user IDs here
ADMIN_IDS = [7019600964, 7985467870]  # <-- Replace with actual admin Telegram user IDs

async def warn_user(user_id, chat_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS warnings (user_id INTEGER, chat_id INTEGER, warns INTEGER, PRIMARY KEY(user_id, chat_id))")
    c.execute("SELECT warns FROM warnings WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
    result = c.fetchone()
    if result:
        warns = result[0] + 1
        c.execute("UPDATE warnings SET warns = ? WHERE user_id = ? AND chat_id = ?", (warns, user_id, chat_id))
    else:
        warns = 1
        c.execute("INSERT INTO warnings (user_id, chat_id, warns) VALUES (?, ?, ?)", (user_id, chat_id, warns))
    conn.commit()
    conn.close()
    return warns

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("❌ This command works only in group chats.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a user's message to warn them.")
        return

    warned_user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    user_id = warned_user.id

    member = await context.bot.get_chat_member(chat_id, user_id)
    if isinstance(member, ChatMemberAdministrator) or isinstance(member, ChatMemberOwner):
        await update.message.reply_text("❌ You cannot warn group admins.")
        return

    warns = warn_user(user_id, chat_id)

    if warns >= 3:
        try:
            await context.bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
            await update.message.reply_text(f"⚠️ {warned_user.mention_html()} has been banned after 3 warnings.", parse_mode="HTML")
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to ban: {e}")
    else:
        await update.message.reply_text(f"⚠️ {warned_user.mention_html()} has been warned ({warns}/3).", parse_mode="HTML")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    db.add_user(chat_id, chat_type)  # Make sure this function avoids duplicates

    caption = (
        f"✨ ᴡᴇʟᴄᴏᴍᴇ {update.effective_user.mention_html()} ᴛᴏ <b>HinataX Support Bot!</b>\n\n"
        "Your smart assistant for group safety & fun!\n\n"
        "⚡ <b>Features Include:</b>\n"
        "• Auto-Moderation & Filters\n"
        "• Welcome / Goodbye Messages\n"
        "• Anti-Spam, Mute, Kick, Ban\n"
        "• Fun & Utility Tools\n"
        "• 24/7 Reliable Support"
    )

    buttons = [
        [
            InlineKeyboardButton("🥀 𝙊𝙬𝙣𝙚𝙧", url="https://t.me/SubunfromHeart"),
            InlineKeyboardButton("🥀 𝙂𝙧𝙤𝙪𝙥", url="https://t.me/animaction_world_in_2025"),
        ],
        [InlineKeyboardButton("🥀 𝘼𝙙𝙙 𝙈𝙚 𝙏𝙤 𝙂𝙧𝙤𝙪𝙥", url=f"https://t.me/{context.bot.username}?startgroup=true")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=WELCOME_IMAGE,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Only admins can use this command.")
        return

    message = " ".join(context.args).strip()
    if not message:
        await update.message.reply_text("⚠️ Please provide a message to broadcast.")
        return

    chats = db.get_all_chats()
    success = 0
    failed = 0

    for chat_id, chat_type in chats:
        try:
            if chat_type in ["group", "supergroup"]:
                await context.bot.send_message(chat_id=chat_id, text=f"📢 <b>Group Broadcast</b>\n\n{message}", parse_mode="HTML")
            else:
                await context.bot.send_message(chat_id=chat_id, text=message)
            success += 1
        except Exception as e:
            print(f"Failed to send to {chat_id} ({chat_type}): {e}")
            failed += 1

    await update.message.reply_text(f"✅ Broadcast complete!\n\nSent: {success}\nFailed: {failed}")

def main():
    db.init_db()
    app = ApplicationBuilder().token(API_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("warn", warn))

    app.run_polling()

if __name__ == "__main__":
    main()