from flask import Flask, send_file, abort
from pyrogram import Client, filters
from pyrogram.types import Message
import os
import json

# ========== CONFIGURAÇÕES ==========
API_ID = 21545360
API_HASH = '25343abde47196a7e4accaf9e6b03437'
BOT_TOKEN = '7669410935:AAFjxaQ7HAgodiX78xwBPZI__yLy0OC1hB4'

app = Flask(__name__)
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ========== CACHE ==========
CACHE_FILE = "cache.json"
DOWNLOAD_FOLDER = "downloads"

# Carrega o cache existente (se houver)
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
else:
    cache = {}

# Garante que a pasta de downloads exista
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ========== BOT ==========
@bot.on_message(filters.video | filters.document & filters.private | filters.group)
async def handle_video(client, message: Message):
    file = message.video or message.document
    if not file:
        return await message.reply("❌ Arquivo inválido.")
    
    file_id = file.file_id
    file_name = file.file_name or f"{file_id}.mp4"
    file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

    # Evita download duplicado
    if file_id not in cache:
        await message.reply("⏬ Baixando o vídeo...")
        await file.download(file_path)

        # Salva no cache
        cache[file_id] = {
            "file_name": file_name,
            "file_path": file_path
        }
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f)

    # Cria o link camuflado
    base_url = "https://mp4rave.onrender.com/video"
    link = f"{base_url}/{file_id}"
    size_mb = round(file.file_size / 1024 / 1024, 2)

    await message.reply(f"✅ Link gerado:\n📁 {file_name}\n📦 {size_mb} MB\n🔗 {link}")

# ========== FLASK ==========
@app.route("/video/<file_id>")
def serve_video(file_id):
    if file_id not in cache:
        return "❌ Arquivo não encontrado no cache.", 404

    file_path = cache[file_id]["file_path"]
    if not os.path.exists(file_path):
        return "❌ Arquivo foi apagado do servidor.", 404

    return send_file(file_path, as_attachment=True)

# ========== INÍCIO ==========
if __name__ == "__main__":
    bot.start()
    app.run(host="0.0.0.0", port=10000)
