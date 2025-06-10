import os
import json
from flask import Flask, send_from_directory
from pyrogram import Client, filters
from pyrogram.types import Message
from threading import Thread
from urllib.parse import quote

# Configurações do Telegram
API_ID = 21545360
API_HASH = "25343abde47196a7e4accaf9e6b03437"
BOT_TOKEN = "7669410935:AAFjxaQ7HAgodiX78xwBPZI__yLy0OC1hB4"

# Caminhos
DOWNLOAD_DIR = "./downloads"
CACHE_FILE = "cache.json"

# Garante que a pasta de downloads existe
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Carrega ou cria o cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
else:
    cache = {}

# Salva o cache atualizado
def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

# Inicializa o bot e o app Flask
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Bot está online com cache!'

@app.route('/video/<path:filename>')
def serve_video(filename):
    if filename in cache:
        return send_from_directory(DOWNLOAD_DIR, filename)
    return "❌ Arquivo não encontrado no cache.", 404

# Flask rodando em thread
def run():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run).start()

# /start
@bot.on_message(filters.command("start"))
async def start_command(bot, message: Message):
    await message.reply_text(
        "👋 Olá! Envie um vídeo ou documento .mp4 e eu vou gerar um link direto pra você."
    )

# Envio de vídeo ou documento
@bot.on_message(filters.video | (filters.document & (filters.private | filters.group)))
async def handle_video(bot, message: Message):
    media = message.video or message.document

    if not media:
        await message.reply("❗ Envie um vídeo ou documento .mp4.")
        return

    filename = media.file_name or "video.mp4"

    if filename in cache:
        # Arquivo já está no cache, só retorna o link
        direct_link = f"https://mp4rave.onrender.com/video/{quote(filename)}"
        await message.reply_text(
            f"🎞️ <b>Nome:</b> <code>{filename}</code>\n"
            f"🔗 <b>Link Direto:</b> <a href='{direct_link}'>{direct_link}</a>",
            parse_mode="html"
        )
        return

    # Faz o download
    file_path = await media.download(file_name=os.path.join(DOWNLOAD_DIR, filename))
    filename = os.path.basename(file_path)

    # Atualiza cache
    cache[filename] = filename
    save_cache()

    # Envia link
    direct_link = f"https://mp4rave.onrender.com/video/{quote(filename)}"
    await message.reply_text(
        f"🎞️ <b>Nome:</b> <code>{filename}</code>\n"
        f"🔗 <b>Link Direto:</b> <a href='{direct_link}'>{direct_link}</a>",
        parse_mode="html"
    )

# Inicia o bot
bot.run()
