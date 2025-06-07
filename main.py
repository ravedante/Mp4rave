from fastapi import FastAPI, Request, Response, Header, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import httpx

app = FastAPI()

API_KEY = "AIzaSyBh-bBd24d6v3yYkALQg61ezICshu61Gv4"

@app.get("/")
def home():
    return {"status": "online"}

# Rota tradicional
@app.get("/video/{file_id}")
async def stream_video(request: Request, file_id: str, range: str = Header(None)):
    return await stream_from_drive(file_id, range)

# Rota estilo Google Drive: /video/d/{id}
@app.get("/video/d/{file_id}")
async def stream_video_drive_style(request: Request, file_id: str, range: str = Header(None)):
    return await stream_from_drive(file_id, range)

async def stream_from_drive(file_id: str, range: str = None):
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={API_KEY}"

    headers = {}
    if range:
        headers["Range"] = range

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(url, headers=headers)
            if r.status_code not in [200, 206]:
                raise HTTPException(status_code=r.status_code, detail="Erro ao acessar o vídeo no Google Drive")

            content_length = r.headers.get("Content-Length")
            content_range = r.headers.get("Content-Range", None)
            status_code = 206 if range else 200

            response_headers = {
                "Content-Type": "video/mp4",
                "Content-Length": content_length or str(len(r.content)),
                "Accept-Ranges": "bytes",
                "Cache-Control": "public, max-age=31536000",  # Cache por 1 ano
                "Content-Disposition": f"attachment; filename={file_id}.mp4"
            }

            if content_range:
                response_headers["Content-Range"] = content_range

            return StreamingResponse(
                iter([r.content]),
                status_code=status_code,
                headers=response_headers
            )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
