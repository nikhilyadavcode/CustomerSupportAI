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
"""

def get_gemini_response(user_message):
    prompt = f"""
{SYSTEM_PROMPT}

Customer: {user_message}

Assistant:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text