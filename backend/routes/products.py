from fastapi import APIRouter
from database.connection import products_collection

router = APIRouter()


@router.get("/products")
def get_all_products():

    products = list(
        products_collection.find(
            {},
            {"_id": 0}
        )
    )

    return products


@router.get("/products/{product_id}")
def get_product(product_id: str):

    product = products_collection.find_one(
        {"product_id": product_id},
        {"_id": 0}
    )

    if product:
        return product

    return {
        "message": "Product not found"
    }