import os
from pyrogram import Client, filters
from pyrogram.types import Message
from urllib.parse import quote
from flask import Flask
from threading import Thread

API_ID = 21545360
API_HASH = "25343abde47196a7e4accaf9e6b03437"
BOT_TOKEN = "7669410935:AAFjxaQ7HAgodiX78xwBPZI__yLy0OC1hB4"

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

app = Flask("")

@app.route('/')
def home():
    return "Bot está online!"

def run():
    app.run(host="0.0.0.0", port=8080)

@bot.on_message(filters.video | (filters.document & (filters.private | filters.group)))
async def handle_video(bot, message: Message):
    media = message.video or message.document
    if not media:
        await message.reply("Envie um vídeo ou documento .mp4.")
        return

    file_path = await media.download()
    file_name = os.path.basename(file_path)
    base_url = "https://mp4rave.onrender.com/video/"
    direct_link = f"{base_url}{quote(file_name)}"

    await message.reply_text(
        f"🎞️ <b>Nome:</b> <code>{file_name}</code>\n"
        f"📸 <b>Link Direto:</b> <a href='{direct_link}'>{direct_link}</a>",
        parse_mode="html"
    )

Thread(target=run).start()
bot.run()
