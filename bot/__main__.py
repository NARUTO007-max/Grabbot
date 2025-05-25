import random
import smtplib
from pyrogram import Client, filters
from pyrogram.types import Message
from email.mime.text import MIMEText

API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = Client("email_bot", api_id=21218274, api_hash=3474a18b61897c672d315fb330edb213, bot_token=8075971963:AAGeCnryaDaYoBcvfXHniFJZiN-_LhikXa0)

# Temporary in-memory storage
user_data = {}
otp_data = {}

SENDER_EMAIL = "shekhikrar026@gmail.com"
SENDER_PASSWORD = "ikkuikku1212"

# START command
@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_photo(
        photo="https://via.placeholder.com/300x150.png?text=Welcome",
        caption="Welcome to the Email Bot! Use /email to start."
    )

# /email command
@bot.on_message(filters.command("email"))
async def email_step_1(client, message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    await message.reply("Please enter your email address:")

    @bot.on_message(filters.private & filters.user(user_id))
    async def get_email(client, msg):
        if "email" not in user_data[user_id]:
            user_data[user_id]["email"] = msg.text
            otp = str(random.randint(100000, 999999))
            otp_data[user_id] = otp
            send_otp_email(msg.text, otp)
            await msg.reply("An OTP has been sent to your email. Please enter it:")

        elif "otp_verified" not in user_data[user_id]:
            if msg.text == otp_data.get(user_id):
                user_data[user_id]["otp_verified"] = True
                await msg.reply("OTP verified! Now send the message you want to email:")
            else:
                await msg.reply("Invalid OTP. Try again:")

        elif "message" not in user_data[user_id]:
            user_data[user_id]["message"] = msg.text
            await msg.reply("Enter the recipient's email address:")

        elif "to_email" not in user_data[user_id]:
            user_data[user_id]["to_email"] = msg.text
            send_final_email(
                from_email=user_data[user_id]["email"],
                to_email=user_data[user_id]["to_email"],
                body=user_data[user_id]["message"]
            )
            await msg.reply("Message successfully sent!")
            del user_data[user_id]
            del otp_data[user_id]

def send_otp_email(to_email, otp):
    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "Your Email Bot OTP"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

def send_final_email(from_email, to_email, body):
    msg = MIMEText(body)
    msg["Subject"] = "Message from Telegram Bot"
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

bot.run()