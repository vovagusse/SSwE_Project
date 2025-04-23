from sqlalchemy import select
from software_shop_webapp.models import *
from software_shop_webapp import db

def get_products() -> list[Product]:
    q = Product.query.all()
    return q


# def get_products_dict() -> list[dict]:
#     ...


def get_product(product_id: int) -> Product:
    q = Product.query.get(product_id)
    return q


# def get_product_dict(product_id: int) -> dict:
#     ...