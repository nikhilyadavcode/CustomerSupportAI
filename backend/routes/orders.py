from fastapi import APIRouter
from database.connection import orders_collection

router = APIRouter()


@router.get("/orders")
def get_all_orders():

    orders = list(
        orders_collection.find(
            {},
            {"_id": 0}
        )
    )

    return orders


@router.get("/orders/{order_id}")
def get_order(order_id: str):

    order = orders_collection.find_one(
        {"order_id": order_id},
        {"_id": 0}
    )

    if order:
        return order

    return {"message": "Order not found"}