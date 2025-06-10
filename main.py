import os
from flask import Flask, send_from_directory
from pyrogram import Client, filters
from pyrogram.types import Message
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

# Página principal (teste)
@app.route('/')
def home():
    return '✅ Bot está online!'

# Rota para servir os vídeos
@app.route('/video/<path:filename>')
def serve_video(filename):
    return send_from_directory('./downloads', filename)

# Thread para manter o Flask rodando
def run():
    app.run(host="0.0.0.0", port=8080)

# Inicia a thread do Flask
Thread(target=run).start()

# Comando /start
@bot.on_message(filters.command("start"))
async def start_command(bot, message: Message):
    await message.reply_text("👋 Olá! Envie um vídeo ou documento .mp4 e eu vou gerar um link direto pra você.")

# Manipula vídeos e documentos enviados
@bot.on_message(filters.video | (filters.document & (filters.private | filters.group)))
async def handle_video(bot, message: Message):
    media = message.video or message.document

    if not media:
        await message.reply("❗ Envie um vídeo ou documento .mp4.")
        return

    download_path = "./downloads"
    os.makedirs(download_path, exist_ok=True)

    file_path = await media.download(file_name=os.path.join(download_path, media.file_name or "video.mp4"))
    file_name = os.path.basename(file_path)
    base_url = "https://mp4rave.onrender.com/video/"
    direct_link = f"{base_url}{quote(file_name)}"

    await message.reply_text(
        f"🎞️ <b>Nome:</b> <code>{file_name}</code>\n"
        f"🔗 <b>Link Direto:</b> <a href='{direct_link}'>{direct_link}</a>",
        parse_mode="html"
    )

# Inicia o bot
bot.run()
