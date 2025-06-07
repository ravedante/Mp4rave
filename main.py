from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import requests
import time
import re

app = FastAPI()

# Cache simples em memória: {mediafire_id: (link, expiração_em_segundos)}
cache = {}

# Função para extrair o link direto do MediaFire
def get_direct_link(mediafire_id: str) -> str:
    url = f"https://www.mediafire.com/file/{mediafire_id}/file"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    match = re.search(r'href="(https://download[^"]+)', response.text)
    if not match:
        raise HTTPException(status_code=404, detail="Link direto não encontrado")

    return match.group(1)

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/video/{mediafire_id}/{filename}")
def serve_video(mediafire_id: str, filename: str):
    now = time.time()

    # Verifica se já está em cache e ainda é válido
    if mediafire_id in cache:
        link, expires_at = cache[mediafire_id]
        if now < expires_at:
            return RedirectResponse(link)
        else:
            del cache[mediafire_id]

    # Busca um novo link
    try:
        direct_link = get_direct_link(mediafire_id)
    except HTTPException as e:
        raise e

    # Armazena no cache por 30 segundos
    cache[mediafire_id] = (direct_link, now + 30)

    return RedirectResponse(direct_link)
