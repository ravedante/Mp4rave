import os
import logging
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

# Dados do bot e API
API_ID = 21545360
API_HASH = "25343abde47196a7e4accaf9e6b03437"
BOT_TOKEN = "7669410935:AAFjxaQ7HAgodiX78xwBPZI__yLy0OC1hB4"

# Configurações
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Gera link direto para o arquivo de vídeo
def gerar_link_direto(msg: Message):
    try:
        file_id = msg.video.file_id if msg.video else msg.document.file_id
        file_name = msg.video.file_name if msg.video else msg.document.file_name
        file_size = msg.video.file_size if msg.video else msg.document.file_size
        tamanho_mb = round(file_size / 1048576, 2)

        return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_id}", file_name, tamanho_mb
    except Exception as e:
        logging.error(f"Erro ao gerar link direto: {e}")
        return None, None, None

# Manipulador de mensagens
@bot.on_message(filters.video | filters.document)
async def salvar_video(_, message: Message):
    if message.video or (message.document and message.document.mime_type.startswith("video/")):
        link, nome, tamanho = gerar_link_direto(message)
        if link:
            await message.reply(
                f"✅ Vídeo salvo com sucesso!\n\n📁 Nome: `{nome}`\n📦 Tamanho: `{tamanho} MB`\n🔗 Link direto: `{link}.mp4`",
                quote=True
            )
        else:
            await message.reply("❌ Ocorreu um erro ao gerar o link.", quote=True)

# Inicia o bot em uma thread separada
def start_bot():
    asyncio.run(bot.start())
    bot.idle()

# Rota básica para manter o servidor vivo
@app.route("/")
def index():
    return "Bot está rodando com sucesso!"

# Inicia o servidor Flask
if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
