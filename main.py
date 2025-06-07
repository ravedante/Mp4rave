from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx

app = FastAPI()

API_KEY = "AIzaSyBh-bBd24d6v3yYkALQg61ezICshu61Gv4"

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/video/{file_id}")
async def stream_video(file_id: str, request: Request):
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={API_KEY}"

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            upstream = await client.get(url, timeout=180.0)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Erro ao conectar com o Google Drive")

        if upstream.status_code == 404:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        if upstream.status_code == 403:
            raise HTTPException(status_code=403, detail="Acesso negado ao arquivo")
        if upstream.status_code != 200:
            raise HTTPException(status_code=upstream.status_code, detail="Erro ao obter o arquivo")

        headers = {
            "Content-Type": upstream.headers.get("Content-Type", "video/mp4"),
            "Content-Length": upstream.headers.get("Content-Length", ""),
            "Cache-Control": "public, max-age=31536000",
            "Content-Disposition": 'inline; filename="video.mp4"',
        }

        return StreamingResponse(
            content=upstream.aiter_bytes(),
            headers=headers,
            media_type=headers["Content-Type"]
        )
