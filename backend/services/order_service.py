from database.connection import orders_collection


def find_order(order_id: str):

    order = orders_collection.find_one(
        {"order_id": order_id},
        {"_id": 0}
    )

    return order