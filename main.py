from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
import re

app = FastAPI()

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/video/{mediafire_id}")
async def get_mediafire_direct_link(mediafire_id: str):
    """
    Ex: /video/abc123456filename
    Onde 'abc123456filename' vem da URL: https://www.mediafire.com/file/abc123456filename
    """
    base_url = f"https://www.mediafire.com/file/{mediafire_id}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(base_url)

        # Expressão regular para pegar o link direto real
        match = re.search(r'https://download[^"]+', response.text)

        if match:
            direct_link = match.group(0)
            return RedirectResponse(url=direct_link)
        else:
            return JSONResponse({"error": "Não foi possível encontrar o link direto."}, status_code=404)

    except Exception as e:
        return JSONResponse({"error": f"Erro ao acessar o link: {str(e)}"}, status_code=500)
