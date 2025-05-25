from pyrogram import Client, filters
from pyrogram.types import Message
from bot.db import setup_db, add_quiz, get_random_quiz
import asyncio
import json
import random

API_ID = 123456    # Replace with your API ID
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
OWNER_ID = 123456789  # Replace with your Telegram ID

app = Client("anime_quiz_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

GROUP_ID = -1001234567890  # Replace with your group ID

setup_db()

# /start command
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("Welcome to the Anime Quiz Bot! Random anime quizzes will be dropped in the group. Use /fdrop to force drop a quiz.")

# /upload command (owner only)
@app.on_message(filters.command("upload") & filters.private)
async def upload_quiz(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("You are not authorized.")

    try:
        parts = message.text.split("\n")
        question = parts[1].strip()
        options = [parts[2], parts[3], parts[4], parts[5]]
        correct = int(parts[6])
        add_quiz(question, options, correct)
        await message.reply("Quiz uploaded successfully.")
    except:
        await message.reply("Format:\n/upload\nQuestion\nOption1\nOption2\nOption3\nOption4\nCorrectIndex (0-3)")

# /fdrop command
@app.on_message(filters.command("fdrop") & filters.group)
async def force_drop(client, message: Message):
    quiz = get_random_quiz()
    if not quiz:
        return await message.reply("No quiz found.")
    await message.chat.send_poll(
        question=quiz["question"],
        options=quiz["options"],
        type="quiz",
        correct_option_id=quiz["correct_option"],
        is_anonymous=False
    )

# Auto drop every random interval
async def auto_drop():
    await app.wait_until_ready()
    while True:
        await asyncio.sleep(random.randint(300, 600))  # Drop every 5 to 10 minutes
        quiz = get_random_quiz()
        if quiz:
            try:
                await app.send_poll(
                    GROUP_ID,
                    question=quiz["question"],
                    options=quiz["options"],
                    type="quiz",
                    correct_option_id=quiz["correct_option"],
                    is_anonymous=False
                )
            except Exception as e:
                print("Failed to send poll:", e)

# Start auto drop loop
@app.on_message(filters.command("start") & filters.user(OWNER_ID))
async def start_auto_drop(client, message: Message):
    await message.reply("Auto quiz drop started.")
    app.loop.create_task(auto_drop())

app.run()