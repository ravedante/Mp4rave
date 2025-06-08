from flask import Flask, send_file, abort, redirect
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder
import os
import requests

BOT_TOKEN = "7669410935:AAFjxaQ7HAgodiX78xwBPZI__yLy0OC1hB4"
app = Flask(__name__)
bot = Bot(BOT_TOKEN)
FILE_LINK_CACHE = {}

@app.route("/video/<file_id>.mp4")
def stream_video(file_id):
    if file_id in FILE_LINK_CACHE:
        file_url = FILE_LINK_CACHE[file_id]
    else:
        try:
            file = bot.get_file(file_id)
            file_url = file.file_path
            FILE_LINK_CACHE[file_id] = file_url
        except:
            return abort(404)
    return redirect(file_url, code=302)

async def start(update: Update, context):
    await update.message.reply_text("Envie um vídeo e eu retornarei um link direto .mp4")

async def handle_video(update: Update, context):
    video = update.message.video or update.message.document
    if not video:
        await update.message.reply_text("Envie um vídeo como documento ou vídeo.")
        return
    file_id = video.file_id
    file_name = (video.file_name or "video") + ".mp4"
    base_url = os.getenv("RENDER_EXTERNAL_URL", "https://seu-projeto.onrender.com")
    await update.message.reply_text(f"🎬 {file_name}\n📎 Link direto:\n{base_url}/video/{file_id}.mp4")

def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
    application.run_polling()

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))