import pytest
import datetime
from software_shop_webapp.models import (
    Product, User, Cart, Image, File, Video,
    Developer, Purchased, Order
)
from software_shop_webapp import db


def test_product_creation(app_context):
    product = Product(title="Test Product", price=50, full_price=60)
    db.session.add(product)
    db.session.commit()

    assert product.product_id is not None
    assert product.title == "Test Product"
    assert product.price == 50
    assert product.full_price == 60

    db.session.delete(product)
    db.session.commit()


def test_user_creation(app_context):
    user = User(login="testuser", password="testpass", full_name="Test User")
    db.session.add(user)
    db.session.commit()

    assert user.user_id is not None
    assert user.login == "testuser"
    assert user.full_name == "Test User"
    assert user.get_id() == user.user_id

    db.session.delete(user)
    db.session.commit()


def test_cart_creation(app_context):
    user = User(login="cartuser", password="pass")
    product = Product(title="Cart Product")
    db.session.add_all([user, product])
    db.session.commit()

    cart_item = Cart(id_user=user.user_id, id_product=product.product_id)
    db.session.add(cart_item)
    db.session.commit()

    assert cart_item.id_user == user.user_id
    assert cart_item.id_product == product.product_id

    db.session.delete(cart_item)
    db.session.delete(product)
    db.session.delete(user)
    db.session.commit()


# def test_image_file_video_creation(app_context):
#     product = Product(title="Media Product")
#     db.session.add(product)
#     db.session.commit()
#
#     image = Image(image_uri="http://example.com/img.png", id_product=product.product_id)
#     file = File(file_uri="D:\\files\\test.zip", id_product=product.product_id)
#     video = Video(video_uri="http://example.com/video.mp4", id_product=product.product_id)
#
#     db.session.add_all([image, file, video])
#     db.session.commit()
#
#     assert image.image_id is not None
#     assert image.id_product == product.product_id
#
#     assert file.file_id is not None
#     assert file.id_product == product.product_id
#
#     assert video.video_id is not None
#     assert video.id_product == product.product_id
#
#     db.session.delete(image)
#     db.session.delete(file)
#     db.session.delete(video)
#     db.session.delete(product)
#     db.session.commit()


def test_developer_creation(app_context):
    user = User(login="devuser", password="pass")
    db.session.add(user)
    db.session.commit()

    developer = Developer(id_user=user.user_id)
    db.session.add(developer)
    db.session.commit()

    assert developer.developer_id is not None
    assert developer.id_user == user.user_id

    db.session.delete(developer)
    db.session.delete(user)
    db.session.commit()


def test_order_and_purchased_creation(app_context):
    user = User(login="buyer", password="pass")
    product = Product(title="Purchased Product", price=150, full_price=170)
    db.session.add_all([user, product])
    db.session.commit()

    order = Order(id_user=user.user_id, card_number="1234567890123456", amount=150, status="completed")
    db.session.add(order)
    db.session.commit()

    purchase = Purchased(
        id_user=user.user_id,
        id_product=product.product_id,
        cost_of_purchase=150.0,
        id_order=order.order_id
    )
    db.session.add(purchase)
    db.session.commit()

    assert order.order_id is not None
    assert purchase.purchase_id is not None
    assert purchase.id_order == order.order_id
    assert purchase.cost_of_purchase == 150.0
    assert isinstance(purchase.time_of_purchase, datetime.datetime)

    # Проверка __repr__
    repr_str = repr(purchase)
    assert str(purchase.purchase_id) in repr_str
    assert str(purchase.cost_of_purchase) in repr_str

    db.session.delete(purchase)
    db.session.delete(order)
    db.session.delete(product)
    db.session.delete(user)
    db.session.commit()
