import re

def detect_intent(message: str):

    text = message.lower()

    # Payment
    if any(word in text for word in [
        "payment",
        "paid",
        "upi",
        "transaction",
        "failed"
    ]):
        return "payment"

    # Refund
    if any(word in text for word in [
        "refund",
        "money back",
        "return money"
    ]):
        return "refund"

    # Order
    if any(word in text for word in [
        "order",
        "delivery",
        "track",
        "shipping"
    ]):
        return "order"

    # Product
    if any(word in text for word in [
        "product",
        "realme",
        "iphone",
        "samsung"
    ]):
        return "product"

    # Ticket
    if any(word in text for word in [
        "ticket",
        "complaint",
        "issue",
        "support"
    ]):
        return "ticket"

    return "general"