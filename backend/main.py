from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid

from database.connection import chat_collection
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
    chat_id: str | None = None


@app.get("/")
def home():
    return {"message": "Backend Running 🚀"}

@app.post("/chat")
def chat(data: ChatRequest):
    try:
        chat_id = data.chat_id or str(uuid.uuid4())

        # Save User Message
        chat_collection.insert_one({
            "chat_id": chat_id,
            "sender": "user",
            "message": data.message,
            "created_at": datetime.utcnow()
        })

        # Gemini Reply
        reply = get_gemini_response(data.message)

        # Save Bot Reply
        chat_collection.insert_one({
            "chat_id": chat_id,
            "sender": "bot",
            "message": reply,
            "created_at": datetime.utcnow()
        })

        return {
            "chat_id": chat_id,
            "reply": reply
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "error": str(e)
        }