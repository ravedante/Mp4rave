from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse, HTMLResponse
import requests
import re

app = FastAPI()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/video/{mediafire_id}/{file_name}")
def get_mediafire_video(mediafire_id: str, file_name: str, response: Response = None):
    try:
        # Monta a URL da página do arquivo no MediaFire
        page_url = f"https://www.mediafire.com/file/{mediafire_id}/file"

        # Requisição à página do MediaFire
        page = requests.get(page_url, headers=HEADERS, timeout=10)
        if page.status_code != 200:
            return HTMLResponse(content="❌ Não foi possível acessar a página do MediaFire.", status_code=502)

        # Extrai o link direto de download usando regex mais robusto
        match = re.search(r'(https://download[^"\']+)', page.text)
        if not match:
            return HTMLResponse(content="❌ Link de download não encontrado na página.", status_code=404)

        direct_link = match.group(1)

        # Adiciona cache para o vídeo
        response.headers["Cache-Control"] = "public, max-age=604800, immutable"

        # Redireciona para o link real de download
        return RedirectResponse(direct_link)

    except Exception as e:
        return HTMLResponse(content=f"❌ Erro inesperado: {str(e)}", status_code=500)
