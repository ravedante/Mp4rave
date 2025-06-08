from flask import Flask, Response, request
import requests

app = Flask(__name__)

BASE_URL = "https://cold-na-phx-4.gofile.io/download/web/"

@app.route('/')
def home():
    return 'Servidor de streaming ativo no Render!'

@app.route('/video/<path:subpath>')
def proxy_video(subpath):
    target_url = BASE_URL + subpath
    headers = {
        "User-Agent": request.headers.get("User-Agent"),
        "Range": request.headers.get("Range")
    }

    try:
        resp = requests.get(target_url, headers=headers, stream=True, timeout=10)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = [(name, value) for (name, value) in resp.headers.items() if name.lower() not in excluded_headers]

        return Response(resp.iter_content(chunk_size=8192),
                        status=resp.status_code,
                        headers=response_headers,
                        content_type=resp.headers.get('Content-Type'))
    except Exception as e:
        return f"Erro ao acessar o vídeo: {e}", 500