import os
from flask import Flask, send_from_directory, jsonify
from pyrogram import Client, filters
from pyrogram.types import Message
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "downloads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

api_id = 21545360
api_hash = "25343abde47196a7e4accaf9e6b03437"
bot_token = "7669410935:AAFjxaQ7HAgodiX78xwBPZI__yLy0OC1hB4"

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@bot.on_message(filters.video | filters.document)
async def save_video(client, message: Message):
    media = message.video or message.document
    if not media or not media.file_name.endswith(".mp4"):
        await message.reply("❌ Apenas arquivos .mp4 são suportados.")
        return

    file_path = await message.download(file_name=os.path.join(UPLOAD_FOLDER, secure_filename(media.file_name)))
    file_size = os.path.getsize(file_path) / (1024 * 1024)
    link = f"https://mp4rave.onrender.com/video/{secure_filename(media.file_name)}"
    await message.reply(f"✅ Vídeo salvo com sucesso!

📁 Nome: `{media.file_name}`
📦 Tamanho: `{file_size:.2f} MB`
🔗 Link: {link}", quote=True)

@app.route("/video/<filename>")
def serve_video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/")
def home():
    return "✅ Seu serviço está ativo 🎉"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)