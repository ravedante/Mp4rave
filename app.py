import os
import json
from flask import Flask, send_from_directory
from pyrogram import Client, filters
from pyrogram.types import Message
from threading import Thread
from urllib.parse import quote

# Credenciais do bot Telegram
API_ID = 21545360
API_HASH = "25343abde47196a7e4accaf9e6b03437"
BOT_TOKEN = "7669410935:AAFjxaQ7HAgodiX78xwBPZI__yLy0OC1hB4"

# Inicialização
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
app = Flask(__name__)

# Diretório de vídeos
DOWNLOAD_FOLDER = "./downloads"
CACHE_FILE = "cache.json"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Carrega o cache se existir
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
else:
    cache = {}

# Página inicial
@app.route('/')
def home():
    return '✅ Bot está online!'

# Rota de vídeo
@app.route('/video/<path:filename>')
def serve_video(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

# Thread do Flask
def run():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run).start()

# Comando /start
@bot.on_message(filters.command("start"))
async def start_command(bot, message: Message):
    await message.reply_text("👋 Olá! Envie um vídeo ou documento .mp4 e eu vou gerar um link direto pra você.")

# Recebe vídeos ou documentos
@bot.on_message(filters.video | (filters.document & (filters.private | filters.group)))
async def handle_video(bot, message: Message):
    media = message.video or message.document

    if not media:
        await message.reply("❗ Envie um vídeo ou documento .mp4.")
        return

    filename = media.file_name or "video.mp4"
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)

    # Faz download
    await media.download(file_name=file_path)

    # Gera link
    link = f"https://mp4rave.onrender.com/video/{quote(filename)}"

    # Salva no cache
    cache[filename] = link
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

    # Responde com link
    await message.reply_text(
        f"🎞️ <b>Nome:</b> <code>{filename}</code>\n"
        f"🔗 <b>Link Direto:</b> <a href='{link}'>{link}</a>",
        parse_mode="html"
    )

# Inicia o bot
bot.run()
