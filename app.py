from flask import Flask, request, Response, stream_with_context, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://tube.xy-space.de/static/web-videos/"

@app.route('/')
def home():
    return jsonify({"status": "online"})

@app.route('/video/<path:video_filename>')
def proxy_video(video_filename):
    video_url = BASE_URL + video_filename

    headers = {
        "Connection": "keep-alive",
        "User-Agent": request.headers.get("User-Agent", "Mozilla/5.0"),
    }

    if 'Range' in request.headers:
        headers['Range'] = request.headers['Range']

    try:
        r = requests.get(video_url, headers=headers, stream=True, timeout=10)
    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar o vídeo: {e}", 500

    if r.status_code not in [200, 206]:
        return f"Erro no servidor de vídeo: {r.status_code}", r.status_code

    def generate():
        for chunk in r.iter_content(chunk_size=4096):
            if chunk:
                yield chunk

    response_headers = {
        "Content-Type": r.headers.get("Content-Type", "video/mp4"),
        "Content-Length": r.headers.get("Content-Length", ""),
        "Content-Range": r.headers.get("Content-Range", ""),
        "Accept-Ranges": "bytes",
        "Connection": "keep-alive",
        "Cache-Control": "public, max-age=3600"
    }

    return Response(stream_with_context(generate()), headers=response_headers, status=r.status_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
