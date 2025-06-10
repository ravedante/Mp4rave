import os
import json
from flask import Flask, send_file, abort
from pyrogram import Client, filters
from pyrogram.types import Message

# CONFIGURAÇÕES
API_ID = 21545360
API_HASH = "25343abde47196a7e4accaf9e6b03437"
BOT_TOKEN = "7669410935:AAFjxaQ7HAgodiX78xwBPZI__yLy0OC1hB4"

app = Flask(__name__)
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

CACHE_FILE = "cache.json"
VIDEO_DIR = "videos"

# Cria cache e pasta se não existirem
if not os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

# Carrega cache
def load_cache():
    with open(CACHE_FILE) as f:
        return json.load(f)

# Salva cache
def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

# Página inicial (resolve erro de "Não encontrado")
@app.route("/")
def home():
    return "Servidor está ativo. Envie um vídeo no grupo."

# Endpoint de vídeo direto
@app.route("/video/<file_id>")
def serve_video(file_id):
    cache = load_cache()
    if file_id in cache:
        filepath = cache[file_id]
        return send_file(filepath, as_attachment=False)
    else:
        return abort(404, "Vídeo não encontrado.")

# Quando alguém envia um vídeo no grupo
@bot.on_message(filters.video | filters.document & filters.private == False)
async def handle_video(client, message: Message):
    media = message.video or message.document
    if not media or not media.file_name.endswith(".mp4"):
        return await message.reply("❌ Envie apenas arquivos .mp4")

    file_id = media.file_id
    file_name = media.file_name

    filepath = os.path.join(VIDEO_DIR, file_id + ".mp4")
    if not os.path.exists(filepath):
        await message.reply("⬇️ Baixando o vídeo...")
        await media.download(filepath)
    
    cache = load_cache()
    cache[file_id] = filepath
    save_cache(cache)

    link = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME', 'localhost')}/video/{file_id}"
    size_mb = round(media.file_size / 1024 / 1024, 2)

    await message.reply(f"✅ <b>{file_name}</b>\n📦 {size_mb} MB\n🔗 <a href='{link}'>{link}</a>", parse_mode="html")

# Inicia tudo
if __name__ == "__main__":
    bot.start()
    app.run(host="0.0.0.0", port=10000)
