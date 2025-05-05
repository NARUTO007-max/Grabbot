from pyrogram import Client, filters
from pyrogram.types import ForceReply
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from bot.db import add_user, is_user_connected, set_connected, add_channel, get_user_channels

bot = Client("PostBot", 
api_id=25698862, 
api_hash="7d7739b44f5f8c825d48cc6787889dbc", bot_token="8118619512:AAGPRtzdpmSLKDx2UOgOC7KtJ6vrgtA63xc")

user_creating_post = {}

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
    return


@bot.on_message(filters.text & filters.private)
async def receive_caption(client, message: Message):
    user_id = message.from_user.id

    # Check if user is in create post flow
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

    # Get media (photo/video)
    if user_id in user_creating_post and 'caption' in user_creating_post[user_id] and 'media' not in user_creating_post[user_id]:
        if message.photo or message.video:
    user_creating_post[user_id]['media'] = message.photo or message.video
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

    # Send to all connected channels
    for channel_id in channels:
        try:
            if data['media']:
                if isinstance(data['media'], list):  # photo is a list of sizes
                    media = data['media'][-1].file_id
                else:
                    media = data['media'][-1].file_id if isinstance(data['media'], list) else data['media'].file_id

if data['media_type'] == 'photo':
    await bot.send_photo(channel_id, photo=media, caption=data['caption'])
else:
    await bot.send_video(channel_id, video=media, caption=data['caption'])
        except Exception as e:
            print(f"Error sending to {channel_id}: {e}")

    await callback_query.message.edit_text("✅ Your post has been sent to all connected channels!")

    user_creating_post.pop(user_id, None)

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    user_id = message.from_user.id
    add_user(user_id)

    if not is_user_connected(user_id):
        # First time setup
        await message.reply_photo(
            photo="https://files.catbox.moe/461mqe.jpg",  # Replace with your image
            caption="Welcome to the Rich Post Bot!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Owner", url="https://t.me/Uzumaki_X_Naruto_6")],
                [InlineKeyboardButton("Group", url="https://t.me/animaction_world_in_2025")],
                [InlineKeyboardButton("Help", callback_data="help")],
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

@bot.on_message(filters.text & filters.regex("^🔗 Connect Channel$"))
async def connect_channel(client, message: Message):
    await message.reply(
        "**To connect a channel:**\n\n1. Add me to your channel as admin.\n2. Promote me with post and edit rights.\n3. Then /start the bot again.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton("/start")]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    set_connected(message.from_user.id, 1)

@bot.on_callback_query(filters.regex("edit_post"))
async def edit_post_cb(client, callback_query):
    user_id = callback_query.from_user.id
    channels = get_user_channels(user_id)

    if not channels:
        await callback_query.message.edit_text(
            "**You haven't connected any channels yet!**\nUse /start and connect one.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="back_to_home")]
            ])
        )
        return

    keyboard = []
    for ch in channels:
        keyboard.append([InlineKeyboardButton(ch, callback_data=f"edit_channel:{ch}")])

    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_home")])

    await callback_query.message.edit_text(
        "**Select a channel to edit its posts:**",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@bot.on_callback_query(filters.regex(r"edit_channel:(.+)"))
async def edit_channel_selected(client, callback_query):
    channel_username = callback_query.data.split(":")[1]

    await callback_query.message.edit_text(
        f"**Editing Channel:** `{channel_username}`\n\n(Feature under development)",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="edit_post")]
        ])
    )

@bot.on_callback_query(filters.regex("back_to_home"))
async def back_to_home_cb(client, callback_query):
    user_id = callback_query.from_user.id

    if is_user_connected(user_id):
        await callback_query.message.edit_text(
            "**Here you can create rich posts, view stats and accomplish other tasks.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📝 Create Post", callback_data="create_post")],
                [InlineKeyboardButton("📊 Channel Stats", callback_data="channel_stats")],
                [InlineKeyboardButton("✏️ Edit Post", callback_data="edit_post")]
            ])
        )
    else:
        await callback_query.message.edit_text(
            "**Please connect a channel to continue.**\n\nUse /start and click '🔗 Connect Channel'",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔁 Try Again", callback_data="back_to_home")]
            ])
        )

@bot.on_callback_query(filters.regex("channel_stats"))
async def channel_stats_cb(client, callback_query):
    user_id = callback_query.from_user.id
    channels = get_user_channels(user_id)  # Ye function list of channel usernames return karega

    if not channels:
        await callback_query.message.edit_text("**You haven't connected any channels yet.**")
        return

    # Inline buttons banao har channel ke liye
    buttons = [[InlineKeyboardButton(text=channel, url=f"https://t.me/{channel}")] for channel in channels]

    # Ek back button bhi add karo
    buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_home")])

    await callback_query.message.edit_text(
        "**Your Connected Channels:**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@bot.on_callback_query(filters.regex("back_to_home"))
async def back_to_home_cb(client, callback_query):
    await callback_query.message.edit_text(
        "**Here you can create rich posts, view stats and accomplish other tasks.**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Create Post", callback_data="create_post")],
            [InlineKeyboardButton("📊 Channel Stats", callback_data="channel_stats")],
            [InlineKeyboardButton("✏️ Edit Post", callback_data="edit_post")],
            [InlineKeyboardButton("Help", callback_data="help")]
        ])
    )

@bot.on_callback_query(filters.regex("help"))
async def help_cb(client, callback_query):
    await callback_query.message.edit_text(
        "**Help Menu**\n\n"
        "- Use '📝 Create Post' to craft a rich post\n"
        "- '✏️ Edit Post' lets you modify existing posts\n"
        "- '📊 Channel Stats' shows how many channels you've connected",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_home")]
        ])
    )

@bot.on_callback_query(filters.regex("back_to_home"))
async def back_to_home_cb(client, callback_query):
    await callback_query.message.edit_text(
        "**Here you can create rich posts, view stats and accomplish other tasks.**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Create Post", callback_data="create_post")],
            [InlineKeyboardButton("📊 Channel Stats", callback_data="channel_stats")],
            [InlineKeyboardButton("✏️ Edit Post", callback_data="edit_post")],
            [InlineKeyboardButton("Help", callback_data="help")]
        ])
    )

if __name__ == "__main__":
    print("[BOT STARTED || 💲💲💲]")
    bot.run()