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

5. If order information or product information is available, ALWAYS use it.

6. Do not ask for the order number again if it is already available.

7. When product information is available, mention:
   - Product Name
   - Brand
   - Price
   - Stock
   - Warranty
   - Category
"""

def get_gemini_response(user_message, context=None):

    prompt = SYSTEM_PROMPT + "\n\n"

    if context:

        if "order" in context:
            order = context["order"]

            prompt += f"""
Order Information:
Order ID: {order.get("order_id")}
Customer: {order.get("customer")}
Product: {order.get("product")}
Price: ₹{order.get("price")}
Payment Status: {order.get("payment_status")}
Delivery Status: {order.get("delivery_status")}
Refund Status: {order.get("refund_status")}

"""

        if "product" in context:
            product = context["product"]

            prompt += f"""
Product Information:
Product ID: {product.get("product_id")}
Name: {product.get("name")}
Brand: {product.get("brand")}
Price: ₹{product.get("price")}
Stock: {product.get("stock")}
Warranty: {product.get("warranty")}
Category: {product.get("category")}
Description: {product.get("description")}

"""

    prompt += f"""
Customer:
{user_message}

Assistant:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text