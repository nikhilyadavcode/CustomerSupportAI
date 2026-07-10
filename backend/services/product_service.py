from database.connection import products_collection


def find_product(product_name: str):

    product = products_collection.find_one(
        {
            "name": {
                "$regex": product_name,
                "$options": "i"
            }
        },
        {
            "_id": 0
        }
    )

    return product