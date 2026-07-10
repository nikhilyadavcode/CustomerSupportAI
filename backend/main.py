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
from routes.products import router as product_router
from services.product_service import find_product
from routes.tickets import router as ticket_router

app = FastAPI()

app.include_router(order_router)
app.include_router(product_router)
app.include_router(ticket_router)

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
        # Find Order
        # -------------------------
        order = None

        match = re.search(r"ORD\d+", data.message.upper())

        if match:
            order = find_order(match.group())

        # -------------------------
        # Find Product
        # -------------------------
        product = None

        product_names = [
            "Realme P4x",
            "Samsung Galaxy S24",
            "iPhone 16"
        ]

        for name in product_names:
            if name.lower() in data.message.lower():
                product = find_product(name)
                break

        # -------------------------
        # Create Context
        # -------------------------
        context = {}

        if order:
            context["order"] = order

        if product:
            context["product"] = product

        # -------------------------
        # Gemini Reply
        # -------------------------
        reply = get_gemini_response(
            data.message,
            context if context else None
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