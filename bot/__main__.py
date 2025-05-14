# main.py
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from db import get_or_create_user, set_character

# Replace with your credentials
app = Client(
    "anime_multiverse_bot",
    api_id=123456,
    api_hash="your_api_hash",
    bot_token="your_bot_token"
)

# Character list (with image links)
CHARACTERS = {
    "Naruto": "https://i.imgur.com/DSQpNRF.jpg",
    "Goku": "https://i.imgur.com/R0D6ZyT.jpg",
    "Luffy": "https://i.imgur.com/V5t6N0v.jpg",
    "Eren": "https://i.imgur.com/KikBl2H.jpg",
    "Sung Jin-Woo": "https://i.imgur.com/MRgFzHt.jpg",
    "Tanjiro": "https://i.imgur.com/O0mM4Nw.jpg",
    "Saitama": "https://i.imgur.com/oqiEQkg.jpg",
    "Asta": "https://i.imgur.com/h6e8grf.jpg"
}

# /start command
@app.on_message(filters.command("start"))
async def start_game(client: Client, message: Message):
    user = get_or_create_user(message.from_user.id, message.from_user.username)

    image_url = "https://i.imgur.com/1kPvBqH.jpg"  # multiverse image
    caption = (
        "**Welcome to Anime Multiverse Battles!**\n\n"
        "Travel through anime universes, choose your hero, "
        "and fight epic villains in turn-based battles.\n\n"
        "_Are you ready to begin your journey?_"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌍 Begin Adventure", callback_data="begin_adventure")]
    ])

    await message.reply_photo(photo=image_url, caption=caption, reply_markup=keyboard)

# Begin Adventure → Show characters
@app.on_callback_query(filters.regex("begin_adventure"))
async def begin_adventure(client: Client, query: CallbackQuery):
    await show_character_selection(client, query.message, query.from_user.id)

# Show one character at a time
async def show_character_selection(client, message, user_id, index=0):
    characters = list(CHARACTERS.items())
    name, image = characters[index]

    buttons = [
        [
            InlineKeyboardButton("✅ Select", callback_data=f"select_{name}"),
        ]
    ]

    if index > 0:
        buttons[0].insert(0, InlineKeyboardButton("⬅️", callback_data=f"char_{index - 1}"))
    if index < len(characters) - 1:
        buttons[0].append(InlineKeyboardButton("➡️", callback_data=f"char_{index + 1}"))

    await message.edit_media(
        media=image,
        caption=f"**{name}**\n\nClick ✅ to choose this hero.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Handle character navigation
@app.on_callback_query(filters.regex(r"char_(\d+)"))
async def paginate_characters(client: Client, query: CallbackQuery):
    index = int(query.matches[0].group(1))
    await show_character_selection(client, query.message, query.from_user.id, index)

# Handle character selection
@app.on_callback_query(filters.regex(r"select_(.+)"))
async def character_selected(client: Client, query: CallbackQuery):
    character = query.matches[0].group(1)
    set_character(query.from_user.id, character)

    await query.message.edit_caption(
        f"✅ You selected **{character}**!\n\nUse /travel to explore universes and start battling!"
    )

# Start the bot
app.run()