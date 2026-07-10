from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid
import re

from routes.orders import router as order_router
from database.connection import chat_collection
from services.gemini_service import get_gemini_response
from services.order_service import find_order

app = FastAPI()

app.include_router(order_router)

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

        # -------------------------
        # Save User Message
        # -------------------------
        chat_collection.insert_one({
            "chat_id": chat_id,
            "sender": "user",
            "message": data.message,
            "created_at": datetime.utcnow()
        })

        # -------------------------
        # Find Order Number
        # -------------------------
        order = None

        match = re.search(r"ORD\d+", data.message.upper())

        if match:
            order = find_order(match.group())

        # -------------------------
        # Gemini Reply
        # -------------------------
        reply = get_gemini_response(
            data.message,
            order
        )

        # -------------------------
        # Save Bot Reply
        # -------------------------
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


# ===========================
# Get Unique Chat History
# ===========================
@app.get("/history")
def get_history():

    chats = list(
        chat_collection.find(
            {"sender": "user"},
            {"_id": 0}
        ).sort("created_at", -1)
    )

    unique_chats = []
    seen = set()

    for chat in chats:

        if chat["chat_id"] not in seen:

            seen.add(chat["chat_id"])

            unique_chats.append({
                "chat_id": chat["chat_id"],
                "title": chat["message"]
            })

    return unique_chats


# ===========================
# Start New Chat
# ===========================
@app.get("/new-chat")
def new_chat():

    return {
        "chat_id": str(uuid.uuid4())
    }


# ===========================
# Load Complete Conversation
# ===========================
@app.get("/history/{chat_id}")
def get_chat(chat_id: str):

    chats = list(
        chat_collection.find(
            {"chat_id": chat_id},
            {"_id": 0}
        ).sort("created_at", 1)
    )

    return chats