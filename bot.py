import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import logging
import shutil

# Configurações
BOT_TOKEN = "7669410935:AAFjxaQ7HAgodiX78xwBPZI__yLy0OC1hB4"
UPLOAD_FOLDER = "videos"
BASE_URL = "https://ravebot.onrender.com/video/"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
logging.basicConfig(level=logging.INFO)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    file = None

    if message.video:
        file = message.video
    elif message.document and message.document.mime_type.startswith("video/"):
        file = message.document

    if file:
        file_id = file.file_id
        file_obj = await context.bot.get_file(file_id)
        file_name = file.file_name or f"{file_id}.mp4"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        await file_obj.download_to_drive(file_path)

        link = BASE_URL + file_name
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        await message.reply_text(f"🎥 Nome: {file_name}
📦 Tamanho: {size_mb:.2f} MB
🔗 Link direto: {link}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
    app.run_polling()
