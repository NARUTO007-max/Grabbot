from bot import bot
from pyrogram import filters
from pyrogram.enums import ChatAction
import os
import io

_DEV_ = 6239769036  # Developer/User ID

# Run shell command and return output
def run(command):
    return os.popen(command).read()

# Command: /logs or /log — tail the log file
@bot.on_message(filters.command(["logs", "log"]) & filters.user(_DEV_))
async def get_logs(_, message):
    run_logs = run("tail log.txt")
    text = await message.reply_text("`Getting logs...`")
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    await message.reply_text(f"```shell\n{run_logs}```")
    await text.delete()

# Command: /flogs or /flog — send full log file as document
@bot.on_message(filters.command(["flogs", "flog"]) & filters.user(_DEV_))
async def get_full_logs(_, message):
    run_logs = run("cat log.txt")
    text = await message.reply_text("`Sending Full logs...`")
    await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
    with io.BytesIO(str.encode(run_logs)) as logs:
        logs.name = "log.txt"
        await message.reply_document(document=logs)
    await text.delete()