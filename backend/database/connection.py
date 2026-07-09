import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)

db = client["customer_support_ai"]

chat_collection = db["chat_history"]

print("✅ MongoDB Connected Successfully")