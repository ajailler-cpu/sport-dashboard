import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Tu es un moteur d'agrégation sportif pour la France.
Retourne un tableau structuré :
Heure | Sport | Catégorie | Événement | Affiche | Diffuseurs | Type diffusion | Intérêt 🇫🇷
"""

def generate():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Programme sport du jour en France"}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = generate()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "table": data
    })
