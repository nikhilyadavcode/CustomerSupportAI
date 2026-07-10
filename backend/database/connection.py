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

# Database
db = client["customer_support_ai"]

# Collections
chat_collection = db["chat_history"]
users_collection = db["users"]
products_collection = db["products"]
orders_collection = db["orders"]
tickets_collection = db["tickets"]