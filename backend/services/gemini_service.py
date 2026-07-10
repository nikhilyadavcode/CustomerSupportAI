import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are a professional AI Customer Support Assistant.

Rules:
1. Greet users politely.
2. Help only with customer support topics:
   - Orders
   - Payments
   - Refunds
   - Delivery
   - Returns
   - Account issues
   - Technical support

3. If the user asks unrelated questions (math, coding, movies, politics, etc.),
reply exactly:

"I'm an AI Customer Support Assistant. Please ask questions related to our products or services."

4. Keep replies short, friendly and professional.

5. If order information is available, ALWAYS use it while answering.

6. Mention Product Name, Payment Status, Delivery Status and Refund Status whenever relevant.

7. Do not ask for the order number again if it is already available.
"""


def get_gemini_response(user_message, order_details=None):

    if order_details:
        order_context = f"""
Order Information:

Order ID: {order_details.get("order_id")}
Customer: {order_details.get("customer")}
Product: {order_details.get("product")}
Price: ₹{order_details.get("price")}
Payment Status: {order_details.get("payment_status")}
Delivery Status: {order_details.get("delivery_status")}
Refund Status: {order_details.get("refund_status")}
"""
    else:
        order_context = "No order information found."

    prompt = f"""
{SYSTEM_PROMPT}

{order_context}

Answer using the order information whenever it is available.
If the customer asks about payment, refund, delivery or product,
refer to the order details in your answer.

Customer:
{user_message}

Assistant:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text