import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from werkzeug.utils import secure_filename

# Configurações fixas do bot
API_ID = 21545360
API_HASH = "25343abde47196a7e4accaf9e6b03437"
BOT_TOKEN = "7669410935:AAFjxaQ7HAgodiX78xwBPZI__yLy0OC1hB4"
BASE_URL = "https://mp4rave.onrender.com"

# Diretório para salvar vídeos
VIDEO_DIR = "videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

# Iniciar o bot
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Atender mensagens com vídeo enviado
@app.on_message(filters.video | filters.document)
async def salvar_video(client: Client, message: Message):
    file = message.video or message.document
    if not file or not file.file_name.endswith(".mp4"):
        await message.reply("❌ Apenas arquivos .mp4 são suportados.")
        return

    nome_seguro = secure_filename(file.file_name)
    caminho = os.path.join(VIDEO_DIR, nome_seguro)
    await message.reply("⏬ Baixando o vídeo...")
    await file.download(file_name=caminho)

    # Gerar link
    link = f"{BASE_URL}/video/{nome_seguro}"
    tamanho_mb = round(file.file_size / (1024 * 1024), 2)
    await message.reply(f"✅ Vídeo salvo com sucesso!\n\n📁 Nome: `{file.file_name}`\n📦 Tamanho: `{tamanho_mb} MB`\n🔗 Link: `{link}`")

# Flask para servir os vídeos
web = Flask(__name__)

@web.route('/')
def index():
    return 'Servidor de vídeos ativo!'

@web.route('/video/<nome>')
def serve_video(nome):
    return web.send_from_directory(VIDEO_DIR, nome)

# Iniciar tudo
if __name__ == "__main__":
    import threading

    def iniciar_flask():
        web.run(host="0.0.0.0", port=10000)

    threading.Thread(target=iniciar_flask).start()
    app.run()
