from pyrogram.types import CallbackQuery

@bot.on_callback_query(filters.regex("refresh"))
async def refresh_handler(client, query: CallbackQuery):
    start = time.time()
    temp = await query.message.reply("Refreshing...")
    ping = (time.time() - start) * 1000
    await temp.delete()

    await query.message.edit_caption(
        caption=(
            "🌿 𝗚𝗥𝗘𝗘𝗧𝗜𝗡𝗚𝗦, 𝗜'𝗠 「ᴡᴀɪғᴜ ɢʀᴀʙʙᴇʀ ʙᴏᴛ」, 𝗡𝗜𝗖𝗘 𝗧𝗢 𝗠𝗘𝗘𝗧 𝗬𝗢𝗨!\n"
            "━━━━━━━━━━━━━━\n"
            "◎ 𝗪𝗛𝗔𝗧 𝗜 𝗗𝗢: 𝗜 𝗦𝗣𝗔𝗪𝗡 𝗪𝗔𝗜𝗙𝗨𝗦 𝗜𝗡 𝗬𝗢𝗨𝗥 𝗖𝗛𝗔𝗧 𝗙𝗢𝗥 𝗨𝗦𝗘𝗥𝗦 𝗧𝗢 𝗖𝗟𝗔𝗜𝗠.\n"
            "◎ 𝗧𝗢 𝗨𝗦𝗘 𝗠𝗘: 𝗔𝗗𝗗 𝗠𝗘 𝗧𝗢 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣 𝗔𝗡𝗗 𝗧𝗔𝗣 𝗧𝗛𝗘 𝗛𝗘𝗟𝗣 𝗕𝗨𝗧𝗧𝗢𝗡 𝗙𝗢𝗥 𝗗𝗘𝗧𝗔𝗜𝗟𝗦.\n"
            "━━━━━━━━━━━━━━\n"
            f"➛ 𝗣𝗜𝗡𝗚: {ping:.2f} ms\n"
            f"➛ 𝗨𝗣𝗧𝗜𝗠𝗘: {get_uptime()}"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ ADD ME ➕", url="https://t.me/YourBotUsername?startgroup=true")],
            [InlineKeyboardButton("🐉 Support group 🐉", url="https://t.me/animaction_world_in_2025"),
             InlineKeyboardButton("🍁 OWNER 🍁", url="https://t.me/Uzumaki_X_Naruto_6")],
            [InlineKeyboardButton("🛡️ HELP ⚡", callback_data="help"),
             InlineKeyboardButton("💲 REFRESH 💲", callback_data="refresh")]
        ])
    )
    await query.answer("Refreshed!")

@bot.on_callback_query(filters.regex("help"))
async def help_handler(client, query: CallbackQuery):
    await query.message.edit_caption(
        caption=(
            "🛡️ **Help Menu**\n\n"
            "› Use me in groups to spawn random waifus.\n"
            "› Members can grab waifus using claim commands.\n"
            "› More features coming soon...\n\n"
            "Use the buttons below to return."
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ])
    )
    await query.answer("Help opened!")

if __name__ == "__main__":
    print("[BOT STARTED||💲💲💲]") 
    bot.run()