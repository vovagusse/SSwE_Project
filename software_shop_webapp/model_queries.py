from models import *


def get_products() -> list[Product]:
    ...


def get_products_dict() -> list[dict]:
    ...


def get_product(product_id: int) -> Product:
    ...


def get_product_dict(product_id: int) -> dict:
    ...