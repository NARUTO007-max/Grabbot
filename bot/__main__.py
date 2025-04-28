from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging
import asyncio

# Bot Token
API_TOKEN = '7851576039:AAFv6o74rF5Ej0DP_aa7AAHgDYXKorkbbj8'  # Replace with your bot token

# Admin ID
YOUR_ADMIN_ID = 7019600964  # Replace with your admin ID

# Group/channel link
GROUP_LINK = "https://t.me/animaction_world_in_2025"  # Apna group link daal

# Owner username
OWNER_USERNAME = "Uzumaki_X_Naruto_6"  # Apna username daal (without @)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command
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

# Callback query handler for close button
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "close":
        try:
            await query.message.delete()
        except Exception as e:
            logger.error(f"Error deleting message: {e}")

# Main function
def main():
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()