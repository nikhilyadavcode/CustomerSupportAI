
import os

BASE_PATH = "knowledge_base"


def read_file(filename):
    path = os.path.join(BASE_PATH, filename)

    with open(path, "r", encoding="utf-8") as file:
        content = file.read().strip()

    return f"📄 {content}"


def get_knowledge(user_message: str):

    message = user_message.lower()

    if "return" in message:
        return read_file("return_policy.txt")

    elif "refund" in message:
        return read_file("refund_policy.txt")

    elif "delivery" in message or "shipping" in message:
        return read_file("delivery_policy.txt")

    elif "track" in message or "cancel" in message or "faq" in message:
        return read_file("faq.txt")

    return None