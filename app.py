from flask import Flask, send_file, abort
from pyrogram import Client, filters
import os
import json

# Credenciais
api_id = 21545360
api_hash = "25343abde47196a7e4accaf9e6b03437"
bot_token = "7669410935:AAFjxaQ7HAgodiX78xwBPZI__yLy0OC1hB4"

# Iniciar bot
app_bot = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Cache JSON
CACHE_FILE = "cache.json"
if not os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "w") as f:
        json.dump({}, f)

def load_cache():
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

# Bot recebe vídeo e gera link
@app_bot.on_message(filters.video | filters.document)
async def handle_video(client, message):
    file_id = message.video.file_id if message.video else message.document.file_id
    file_name = message.video.file_name if message.video else message.document.file_name
    file_path = f"downloads/{file_id}.mp4"

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    cache = load_cache()
    if file_id in cache:
        await message.reply_text(f"🎥 {cache[file_id]['name']} ({cache[file_id]['size']})\n🔗 https://mp4rave.onrender.com/video/{file_id}")
        return

    msg = await message.reply_text("⬇️ Baixando vídeo...")

    file = await client.download_media(message, file_path)
    file_size = os.path.getsize(file_path)
    readable_size = f"{file_size / (1024 * 1024):.2f} MB"

    cache[file_id] = {
        "path": file_path,
        "name": file_name,
        "size": readable_size
    }
    save_cache(cache)

    await msg.edit_text(
        f"✅ Vídeo salvo!\n\n🎬 Nome: {file_name}\n📦 Tamanho: {readable_size}\n🔗 Link: https://mp4rave.onrender.com/video/{file_id}"
    )

# Servidor Flask
app = Flask(__name__)

@app.route("/video/<file_id>")
def serve_video(file_id):
    cache = load_cache()
    if file_id in cache:
        path = cache[file_id]["path"]
        return send_file(path, mimetype="video/mp4")
    return "❌ Arquivo não encontrado no cache.", 404

# Início
if __name__ == "__main__":
    import threading
    threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 10000}).start()
    app_bot.run()
