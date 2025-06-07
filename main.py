from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

API_KEY = "AIzaSyBh-bBd24d6v3yYkALQg61ezICshu61Gv4"

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/video/{file_id}", response_class=HTMLResponse)
def intermediate_download_page(file_id: str, request: Request):
    # Adiciona parâmetro fake para camuflar o tráfego
    fake_param = "utm=" + request.client.host.replace(".", "")[-4:]
    drive_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={API_KEY}&{fake_param}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="3;url={drive_url}">
        <title>Preparando download...</title>
    </head>
    <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
        <h2>Aguarde um momento...</h2>
        <p>Seu vídeo está sendo preparado. O download começará em instantes.</p>
        <p><a href="{drive_url}" download>Clique aqui se não for redirecionado</a></p>
    </body>
    </html>
    """
    
    headers = {
        "Cache-Control": "public, max-age=86400",  # 1 dia de cache
        "Content-Type": "text/html; charset=UTF-8"
    }
    
    return HTMLResponse(content=html_content, headers=headers)

@app.get("/video/d/{file_id}")
def legacy_redirect(file_id: str, request: Request):
    fake_param = "ref=" + request.client.host.replace(".", "")[-4:]
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={API_KEY}&{fake_param}"
    headers = {"Cache-Control": "public, max-age=86400"}
    return RedirectResponse(url=url, status_code=307, headers=headers)
