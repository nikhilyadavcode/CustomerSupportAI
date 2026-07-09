from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from services.gemini_service import get_gemini_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "Backend Running 🚀"}


@app.post("/chat")
def chat(data: ChatRequest):

    reply = get_gemini_response(data.message)

    return {
        "reply": reply
    }