from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from software_shop_webapp.models import *
from software_shop_webapp import db
import pprint


def get_products() -> list[Product]:
    q = Product.query.all()
    return q


def get_products_in_cart(user_id: int) -> list[Product]:
    q = select(
            Product
        ).join(
            Cart, Product.product_id == Cart.id_product
        ).where(
            Cart.id_user == user_id
        )
    sth = db.session.execute(q)
    obj = sth.all()
    return obj

def add_product_to_cart(user_id: int, product_id: int) -> None:
    try:
        q = insert(
                Cart
            ).values(
                id_product=product_id,
                id_user=user_id
            )
        db.session.execute(q)
        db.session.commit()
    except IntegrityError:
        print(":(")

def delete_product_from_cart(user_id: int, product_id: int) -> None:
    q = delete(
            Cart
        ).where(
            Cart.id_product==product_id,
            Cart.id_user==user_id
        )
    db.session.execute(q)
    db.session.commit()


# def get_products_dict() -> list[dict]:
#     ...


def get_product(product_id: int) -> Product:
    q = Product.query.get({"product_id": product_id})
    return q


# def get_product_dict(product_id: int) -> dict:
#     ...