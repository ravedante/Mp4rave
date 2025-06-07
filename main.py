from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
import httpx
import asyncio

app = FastAPI()

API_KEY = "AIzaSyBh-bBd24d6v3yYkALQg61ezICshu61Gv4"

@app.get("/", response_class=JSONResponse)
async def root():
    return {"status": "online"}

@app.get("/video/{file_id}")
async def stream_video(request: Request, file_id: str):
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={API_KEY}"

    headers = {}
    range_header = request.headers.get("range")
    if range_header:
        headers["Range"] = range_header

    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
        try:
            resp = await client.get(url, headers=headers)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Erro ao conectar ao Google Drive")

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")
    elif resp.status_code == 403:
        raise HTTPException(status_code=403, detail="Acesso negado ao vídeo")
    elif resp.status_code not in (200, 206):
        raise HTTPException(status_code=resp.status_code, detail="Erro ao obter vídeo")

    content_length = resp.headers.get("Content-Length")
    content_type = resp.headers.get("Content-Type", "video/mp4")
    content_range = resp.headers.get("Content-Range")

    # Headers para resposta ao cliente
    response_headers = {
        "Content-Type": content_type,
        "Cache-Control": "public, max-age=31536000",
        "Accept-Ranges": "bytes",
    }
    if content_range:
        response_headers["Content-Range"] = content_range
    if content_length:
        response_headers["Content-Length"] = content_length

    async def video_iterator():
        async for chunk in resp.aiter_bytes(chunk_size=1024*1024):
            yield chunk
            await asyncio.sleep(0)

    return StreamingResponse(video_iterator(), status_code=resp.status_code, headers=response_headers)
