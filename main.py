from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from groq import Groq
import os

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/chat.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
async def chat(data: dict):
    user_message = data.get("message")

    if not user_message:
        return {"reply": "Please type something"}

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    )

    return {"reply": response.choices[0].message.content}
