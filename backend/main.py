from fastapi import FastAPI, Header
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid
import re

from routes.orders import router as order_router
from routes.products import router as product_router
from routes.tickets import router as ticket_router
from routes.auth import router as auth_router

from database.connection import chat_collection
from database.users import users_collection

from services.gemini_service import get_gemini_response
from services.order_service import find_order
from services.product_service import find_product
from services.ticket_service import create_ai_ticket
from services.auth_service import verify_token

from ai.intent_detector import detect_intent

app = FastAPI()

app.include_router(order_router)
app.include_router(product_router)
app.include_router(ticket_router)
app.include_router(auth_router)

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
def chat(
    data: ChatRequest,
    authorization: str = Header(default=None)
):
    try:

        # -------------------------
        # Logged-in User
        # -------------------------
        user = None

        if authorization:
            token = authorization.replace("Bearer ", "")
            email = verify_token(token)

            if email:
                user = users_collection.find_one(
                    {"email": email},
                    {"password": 0}
                )

        chat_id = data.chat_id or str(uuid.uuid4())

        # -------------------------
        # Save User Message
        # -------------------------
        chat_collection.insert_one({
            "chat_id": chat_id,
            "sender": "user",
            "message": data.message,
            "user": user["email"] if user else None,
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
        # Context
        # -------------------------
        context = {}

        if order:
            context["order"] = order

        if product:
            context["product"] = product

        # -------------------------
        # Intent Detection
        # -------------------------
        intent = detect_intent(data.message)

        message = data.message.lower()

        create_ticket_keywords = [
            "create ticket",
            "raise ticket",
            "open ticket",
            "support ticket",
            "register complaint",
            "file complaint",
            "create complaint"
        ]

        should_create_ticket = any(
            keyword in message
            for keyword in create_ticket_keywords
        )

        # -------------------------
        # Create Ticket
        # -------------------------
        if should_create_ticket:

            ticket = create_ai_ticket(
                issue=intent.title(),
                description=data.message
            )

            reply = f"""
✅ Support Ticket Created Successfully

Ticket ID: {ticket['ticket_id']}

Issue: {ticket['issue']}

Status: {ticket['status']}

Priority: {ticket['priority']}

Our support team will contact you shortly.
"""

        else:

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
            "user": user["email"] if user else None,
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