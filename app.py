from flask import Flask, request, Response, stream_with_context, jsonify
import requests

app = Flask(__name__)

# Substitua pelo template do link streaming MP4 do seu PeerTube,
# coloque {id} onde deve entrar o ID do vídeo
VIDEO_URL_TEMPLATE = "https://seu-peertube.com/videos/watch/{id}/video.mp4"

@app.route('/')
def home():
    return jsonify({"status": "online"})

@app.route('/video/<video_id>')
def proxy_video(video_id):
    video_url = VIDEO_URL_TEMPLATE.format(id=video_id)

    headers = {}
    if 'Range' in request.headers:
        headers['Range'] = request.headers['Range']

    try:
        r = requests.get(video_url, headers=headers, stream=True)
    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar o vídeo: {e}", 500

    if r.status_code not in [200, 206]:
        return f"Erro no servidor de vídeo: {r.status_code}", r.status_code

    def generate():
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                yield chunk

    response_headers = {}
    for header in ['Content-Type', 'Content-Length', 'Content-Range', 'Accept-Ranges', 'Cache-Control']:
        if header in r.headers:
            response_headers[header] = r.headers[header]

    return Response(stream_with_context(generate()), headers=response_headers, status=r.status_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
