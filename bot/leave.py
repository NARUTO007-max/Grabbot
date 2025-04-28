from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Bot Token
API_TOKEN = 'YOUR_BOT_TOKEN'  # Your bot token

# Admin ID (change it to your admin user ID)
YOUR_ADMIN_ID = 123456789  # Replace with your admin ID

# Group/channel ID (for broadcast command)
YOUR_CHANNEL_ID = "@your_channel_id"  # Replace with your channel or group ID

# Enable logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

@bot.on_message(filters.command(["broadcast", "bcast"]) & filters.user(OWNER_IDS))
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