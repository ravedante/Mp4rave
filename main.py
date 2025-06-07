from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import httpx
import re

app = FastAPI()

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/video/{file_id}")
async def get_video(file_id: str):
    try:
        # Monta a URL da página do MediaFire com base no ID fornecido
        mediafire_url = f"https://www.mediafire.com/file/{file_id}"

        # Faz a requisição HTTP simulando um navegador
        async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
            response = await client.get(mediafire_url)

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado no MediaFire")

        # Procura o link de download direto no HTML da página
        match = re.search(r'href="(https://download[^"]+)"', response.text)
        if not match:
            raise HTTPException(status_code=404, detail="Link de download direto não encontrado")

        download_link = match.group(1)
        return RedirectResponse(url=download_link)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")
