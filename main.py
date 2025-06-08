from flask import Flask, request, redirect
import os

app = Flask(__name__)

@app.route("/video/<path:video_id>")
def stream_proxy(video_id):
    base_url = "https://cold-na-phx-4.gofile.io/download/web/"
    video_url = f"{base_url}{video_id}"
    return redirect(video_url, code=302)

@app.route("/")
def index():
    return "🟢 Proxy online e pronto para streaming de vídeos MP4 do Gofile."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
