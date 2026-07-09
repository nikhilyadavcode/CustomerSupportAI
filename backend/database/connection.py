from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)

try:
    client.admin.command("ping")
    print("✅ MongoDB Authentication Successful")
except Exception as e:
    print("❌ MongoDB Error:", e)

db = client["customer_support_ai"]
chat_collection = db["chat_history"]