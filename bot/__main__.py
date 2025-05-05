from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from bot.db import add_user, is_user_connected, set_connected, add_channel, get_user_channels

bot = Client("PostBot", 
    api_id=25698862, 
    api_hash="7d7739b44f5f8c825d48cc6787889dbc", 
    bot_token="8118619512:AAGPRtzdpmSLKDx2UOgOC7KtJ6vrgtA63xc"
)

user_creating_post = {}

# Start command
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    user_id = message.from_user.id
    add_user(user_id)

    if not is_user_connected(user_id):
        await message.reply_photo(
            photo="https://files.catbox.moe/461mqe.jpg",
            caption="Welcome to the Rich Post Bot!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Owner", url="https://t.me/Uzumaki_X_Naruto_6")],
                [InlineKeyboardButton("Group", url="https://t.me/animaction_world_in_2025")],
                [InlineKeyboardButton("Help", callback_data="help")]
            ])
        )
        await message.reply(
            "Please connect a channel to continue.",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("🔗 Connect Channel")]],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
    else:
        await message.reply(
            "**Here you can create rich posts, view stats and accomplish other tasks.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📝 Create Post", callback_data="create_post")],
                [InlineKeyboardButton("📊 Channel Stats", callback_data="channel_stats")],
                [InlineKeyboardButton("✏️ Edit Post", callback_data="edit_post")]
            ])
        )

# Connect channel
@bot.on_message(filters.text & filters.regex("^🔗 Connect Channel$"))
async def connect_channel(client, message: Message):
    await message.reply(
        "**To connect a channel:**\n\n1. Add me to your channel as admin.\n2. Promote me with post and edit rights.\n3. Then /start the bot again.",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("/start")]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    set_connected(message.from_user.id, 1)

# Create post flow
@bot.on_callback_query(filters.regex("create_post"))
async def create_post_cb(client, callback_query):
    user_id = callback_query.from_user.id
    user_creating_post[user_id] = {}

    await callback_query.message.edit_text(
        "**Let's create a rich post!**\n\nPlease send the **caption** for your post (you can use markdown):",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_home")]
        ])
    )

# Caption input
@bot.on_message(filters.text & filters.private)
async def receive_caption(client, message: Message):
    user_id = message.from_user.id

    if user_id in user_creating_post and 'caption' not in user_creating_post[user_id]:
        user_creating_post[user_id]['caption'] = message.text

        await message.reply(
            "**Got it! Now send the photo or video you'd like to include in the post.**",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("⬅️ Cancel")]],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
        return

    if user_id in user_creating_post and 'caption' in user_creating_post[user_id] and 'media' not in user_creating_post[user_id]:
        if message.photo or message.video:
            media = message.photo or message.video
            user_creating_post[user_id]['media'] = media
            user_creating_post[user_id]['media_type'] = 'photo' if message.photo else 'video'

            await message.reply(
                "**Your post is ready! Do you want to send it now to a connected channel?**",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ Yes, Send", callback_data="confirm_post")],
                    [InlineKeyboardButton("❌ Cancel", callback_data="back_to_home")]
                ])
            )
        else:
            await message.reply("Please send a valid photo or video.")

# Send post
@bot.on_callback_query(filters.regex("confirm_post"))
async def confirm_post_cb(client, callback_query):
    user_id = callback_query.from_user.id
    data = user_creating_post.get(user_id)

    if not data or 'media' not in data or 'caption' not in data:
        await callback_query.answer("Post data incomplete.", show_alert=True)
        return

    channels = get_user_channels(user_id)
    if not channels:
        await callback_query.message.edit_text(
            "**No channel connected!** Use /start and '🔗 Connect Channel' to connect a channel.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back_to_home")]])
        )
        return

    for channel_id in channels:
        try:
            media = data['media'][-1].file_id if isinstance(data['media'], list) else data['media'].file_id

            if data['media_type'] == 'photo':
                await bot.send_photo(channel_id, photo=media, caption=data['caption'])
            else:
                await bot.send_video(channel_id, video=media, caption=data['caption'])

        except Exception as e:
            print(f"Error sending to {channel_id}: {e}")

    await callback_query.message.edit_text("✅ Your post has been sent to all connected channels!")
    user_creating_post.pop(user_id, None)

# Back to Home
@bot.on_callback_query(filters.regex("back_to_home"))
async def back_to_home_cb(client, callback_query):
    user_id = callback_query.from_user.id

    if is_user_connected(user_id):
        await callback_query.message.edit_text(
            "**Here you can create rich posts, view stats and accomplish other tasks.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📝 Create Post", callback_data="create_post")],
                [InlineKeyboardButton("📊 Channel Stats", callback_data="channel_stats")],
                [InlineKeyboardButton("✏️ Edit Post", callback_data="edit_post")],
                [InlineKeyboardButton("Help", callback_data="help")]
            ])
        )
    else:
        await callback_query.message.edit_text(
            "**Please connect a channel to continue.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔁 Try Again", callback_data="back_to_home")]
            ])
        )

# Help
@bot.on_callback_query(filters.regex("help"))
async def help_cb(client, callback_query):
    await callback_query.message.edit_text(
        "**Help Menu**\n\n"
        "- 📝 Create Post: Craft a rich post.\n"
        "- ✏️ Edit Post: Modify your posts.\n"
        "- 📊 Channel Stats: View connected channels.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_home")]
        ])
    )

# Start the bot
bot.run()