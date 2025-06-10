
import os  
from flask import Flask, send_from_directory  
from pyrogram import Client, filters  
from pyrogram.types import Message  
from pyrogram.enums import ParseMode  
from threading import Thread  
from urllib.parse import quote  
  
# Dados da sua aplicação Telegram  
API_ID = 21545360  
API_HASH = "25343abde47196a7e4accaf9e6b03437"  
BOT_TOKEN = "7669410935:AAFjxaQ7HAgodiX78xwBPZI__yLy0OC1hB4"  
  
# Criação do bot Pyrogram  
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)  
  
# Inicializa o Flask  
app = Flask(__name__)  
  
@app.route('/')  
def home():  
    return '✅ Bot está online!'  
  
@app.route('/video/<path:filename>')  
def serve_video(filename):  
    return send_from_directory('./downloads', filename)  
  
def run():  
    app.run(host="0.0.0.0", port=8080)  
  
Thread(target=run).start()  
  
@bot.on_message(filters.command("start"))  
async def start_command(bot, message: Message):  
    await message.reply_text("👋 Envie um vídeo ou documento .mp4 e eu enviarei um link direto!")  
  
@bot.on_message(filters.video | filters.document)  
async def handle_video(bot, message: Message):  
    media = message.video or message.document  
  
    if not media or (media.mime_type and not media.mime_type.startswith("video/")):  
        await message.reply("❗ Envie um arquivo de vídeo válido (.mp4).")  
        return  
  
    download_path = "./downloads"  
    os.makedirs(download_path, exist_ok=True)  
  
    file_name = media.file_name or f"{media.file_unique_id}.mp4"  
    file_path = os.path.join(download_path, file_name)  
  
    await bot.download_media(message, file_path)  
  
    base_url = "https://mp4rave.onrender.com/video/"  
    direct_link = f"{base_url}{quote(file_name)}"  
  
    await message.reply_text(  
        f"🎞️ <b>Nome:</b> <code>{file_name}</code>\n"  
        f"🔗 <b>Link Direto:</b> <a href='{direct_link}'>{direct_link}</a>",  
        parse_mode=ParseMode.HTML  
    )  
  
bot.run()
