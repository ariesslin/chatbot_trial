import openai
import os
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated
from dotenv import load_dotenv
from mangum import Mangum

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

chat_log = [{"role": "system", "content": "You are a Python tutor AI, \
            completely dedicated to helping students learn Python from scratch."}]
chat_responses = []

app = FastAPI()
handler = Mangum(app)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})

@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):
    chat_log.append({"role": "user", "content": user_input})
    chat_responses.append(user_input)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_log,
        temperature=0.6,
    )

    bot_response = response['choices'][0]['message']['content']
    chat_log.append({"role": "assistant", "content": bot_response})
    chat_responses.append(bot_response)
    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})

@app.get("/image", response_class=HTMLResponse)
async def image_page(request: Request):
    return templates.TemplateResponse("image.html", {"request": request})

@app.post("/image", response_class=HTMLResponse)
async def create_image(request: Request, user_input: Annotated[str, Form()]):
    response = openai.Image.create(
        prompt=user_input,
        n=1,
        size="512x512",
    )
    image_url = response['data'][0]['url']
    return templates.TemplateResponse("image.html", {"request": request, "image_url": image_url})