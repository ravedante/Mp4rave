from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

API_KEY = "AIzaSyBh-bBd24d6v3yYkALQg61ezICshu61Gv4"

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/video/{file_id}")
def redirect_to_drive(file_id: str):
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={API_KEY}"
    return RedirectResponse(url)
