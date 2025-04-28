from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import asyncio

# Bot Token
API_TOKEN = '7851576039:AAFv6o74rF5Ej0DP_aa7AAHgDYXKorkbbj8'  # Replace with your bot token

# Admin ID (change it to your admin user ID)
YOUR_ADMIN_ID = 7019600964  # Replace with your admin ID

# Group/channel ID (for broadcast command)
YOUR_CHANNEL_ID = "-1002600495465"  # Replace with your channel or group ID

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Broadcast function
async def broadcast(update: Update, context: CallbackContext):
    # Only allow admin to send broadcast messages
    if update.message.from_user.id == YOUR_ADMIN_ID:
        message = " ".join(context.args)  # Collect arguments
        if message:
            # For now, using in-memory list of users (replace with database for large scale)
            users = [{"_id": YOUR_ADMIN_ID}]  # Add actual user IDs here
            success = 0
            failed = 0

            for user in users:
                try:
                    await update.message.bot.send_message(chat_id=user["_id"], text=message)
                    success += 1
                    await asyncio.sleep(0.1)
                except Exception as e:
                    logger.error(f"Failed to send message to {user['_id']}: {e}")
                    failed += 1

            await update.message.reply(f"✅ Broadcast sent to {success} users.\n❌ Failed to send to {failed} users.")
        else:
            await update.message.reply("❌ Please provide a message to broadcast.")
    else:
        await update.message.reply("❌ You are not authorized to use this command.")

# Goodbye message for when someone leaves the group
async def user_left(update: Update, context: CallbackContext):
    if update.message.left_chat_member:
        user = update.message.left_chat_member
        user_name = user.username if user.username else "Unknown"
        user_profile_pic = (await context.bot.get_user_profile_photos(user.id)).photos[0][-1].file_id
        goodbye_message = f"Sad to see you go, {user_name}! Hope you return soon! 👋"
        await update.message.reply_photo(photo=user_profile_pic, caption=goodbye_message)

# Main function to run the bot
def main():
    application = Application.builder().token(API_TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("broadcast", broadcast))

    # Handler for user leaving the group
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, user_left))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
