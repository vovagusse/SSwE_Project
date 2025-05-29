import os
import sys
import pytest
import datetime
from sqlite3 import IntegrityError

sys.path.insert(0, os.path.abspath("../"))
# sys.path.insert(0, os.path.abspath("../../software_shop_webapp"))  # Альтернативный путь при необходимости

from software_shop_webapp import db
from software_shop_webapp.models import (
    Product, User, Cart, Image, File, Video,
    Developer, Purchased, Order, load_user
)

# ---------- Тесты моделей ----------

def test_product_creation(app_context):
    """Создание и удаление продукта"""
    user = User.query.get(5001)
    if not user:
        user = User(user_id=5001, login="super_admin", password="password", is_developer=True)
        db.session.add(user)
        db.session.commit()

    developer = Developer.query.get(5001)
    if not developer:
        developer = Developer(developer_id=5001, developer_name="admin-dev", id_user=user.user_id)
        db.session.add(developer)
        db.session.commit()

    product = Product.query.get(5001)
    if not product:
        product = Product(
            product_id=5001,
            title="Test Product",
            price=50,
            full_price=60,
            id_developer=developer.developer_id
        )
        db.session.add(product)
        db.session.commit()

    assert product.product_id is not None
    assert product.title == "Test Product"
    assert product.price == 50
    assert product.full_price == 60

    db.session.delete(product)
    db.session.delete(developer)
    db.session.delete(user)
    db.session.commit()


def test_user_creation(app_context):
    """Создание и удаление пользователя"""
    user = User.query.get(5001)
    if not user:
        user = User(
            user_id=5001,
            login="super_admin",
            password="password",
            full_name="Test User",
            is_developer=False
        )
        db.session.add(user)
        db.session.commit()

    assert user.user_id is not None
    assert user.login == "super_admin"
    assert user.full_name == "Test User"
    assert user.get_id() == user.user_id

    db.session.delete(user)
    db.session.commit()


def test_cart_creation(app_context):
    """Добавление продукта в корзину"""
    user = User.query.get(5001)
    if not user:
        user = User(user_id=5001, login="super_admin", password="password", full_name="Test User", is_developer=False)
        db.session.add(user)
        db.session.commit()

    developer = Developer.query.get(5001)
    if not developer:
        developer = Developer(developer_id=5001, developer_name="admin-dev", id_user=user.user_id)
        db.session.add(developer)
        db.session.commit()

    product = Product.query.get(5001)
    if not product:
        product = Product(product_id=5001, title="Test Product", price=50, full_price=60, id_developer=developer.developer_id)
        db.session.add(product)
        db.session.commit()

    cart_item = Cart(id_user=user.user_id, id_product=product.product_id)
    db.session.add(cart_item)
    db.session.commit()

    assert cart_item.id_user == user.user_id
    assert cart_item.id_product == product.product_id

    db.session.delete(cart_item)
    db.session.delete(product)
    db.session.delete(developer)
    db.session.delete(user)
    db.session.commit()


def test_developer_creation(app_context):
    """Создание разработчика"""
    user = User.query.get(5001)
    if not user:
        user = User(user_id=5001, login="super_admin", password="password", full_name="Test User", is_developer=False)
        db.session.add(user)
        db.session.commit()

    developer = Developer.query.get(5001)
    if not developer:
        developer = Developer(developer_id=5001, developer_name="admin-dev", id_user=user.user_id)
        db.session.add(developer)
        db.session.commit()

    assert developer.developer_id is not None
    assert developer.id_user == user.user_id

    db.session.delete(developer)
    db.session.delete(user)
    db.session.commit()


def test_order_and_purchased_creation(app_context):
    """Создание заказа и покупки"""
    user = User.query.get(5001)
    if not user:
        user = User(user_id=5001, login="super_admin", password="password", full_name="Test User", is_developer=False)
        db.session.add(user)
        db.session.commit()

    developer = Developer.query.get(5001)
    if not developer:
        developer = Developer(developer_id=5001, developer_name="admin-dev", id_user=user.user_id)
        db.session.add(developer)
        db.session.commit()

    product = Product.query.get(5001)
    if not product:
        product = Product(product_id=5001, title="Test Product", price=50, full_price=60, id_developer=developer.developer_id)
        db.session.add(product)
        db.session.commit()

    order = Order.query.get(5001)
    if not order:
        order = Order(
            order_id=5001,
            id_user=user.user_id,
            card_number="1234567890123456",
            amount=150,
            status="completed"
        )
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
    db.session.delete(developer)
    db.session.delete(user)
    db.session.commit()


def test_file_creation(app_context):
    """Создание и удаление файла"""
    # Создаем необходимые сущности
    user = User.query.get(5002)
    if not user:
        user = User(user_id=5002, login="file_user", password="password")
        db.session.add(user)
        db.session.commit()

    developer = Developer.query.get(5002)
    if not developer:
        developer = Developer(developer_id=5002, developer_name="file-dev", id_user=user.user_id)
        db.session.add(developer)
        db.session.commit()

    product = Product.query.get(5002)
    if not product:
        product = Product(product_id=5002, title="File Product", price=100, full_price=120, id_developer=developer.developer_id)
        db.session.add(product)
        db.session.commit()

    file = File(file_uri="D:\\files\\TestFile.7z", id_product=product.product_id)
    db.session.add(file)
    db.session.commit()

    assert file.file_id is not None
    assert file.file_uri == "D:\\files\\TestFile.7z"
    assert file.id_product == product.product_id

    db.session.delete(file)
    db.session.delete(product)
    db.session.delete(developer)
    db.session.delete(user)
    db.session.commit()


def test_image_creation(app_context):
    """Создание и удаление изображения"""
    user = User.query.get(5003)
    if not user:
        user = User(user_id=5003, login="image_user", password="password")
        db.session.add(user)
        db.session.commit()

    developer = Developer.query.get(5003)
    if not developer:
        developer = Developer(developer_id=5003, developer_name="image-dev", id_user=user.user_id)
        db.session.add(developer)
        db.session.commit()

    product = Product.query.get(5003)
    if not product:
        product = Product(product_id=5003, title="Image Product", price=110, full_price=130, id_developer=developer.developer_id)
        db.session.add(product)
        db.session.commit()

    image = Image(image_uri="https://example.com/image.png", id_product=product.product_id)
    db.session.add(image)
    db.session.commit()

    assert image.image_id is not None
    assert image.image_uri == "https://example.com/image.png"
    assert image.id_product == product.product_id

    db.session.delete(image)
    db.session.delete(product)
    db.session.delete(developer)
    db.session.delete(user)
    db.session.commit()


def test_video_creation(app_context):
    """Создание и удаление видео"""
    user = User.query.get(5004)
    if not user:
        user = User(user_id=5004, login="video_user", password="password")
        db.session.add(user)
        db.session.commit()

    developer = Developer.query.get(5004)
    if not developer:
        developer = Developer(developer_id=5004, developer_name="video-dev", id_user=user.user_id)
        db.session.add(developer)
        db.session.commit()

    product = Product.query.get(5004)
    if not product:
        product = Product(product_id=5004, title="Video Product", price=120, full_price=140, id_developer=developer.developer_id)
        db.session.add(product)
        db.session.commit()

    video = Video(video_uri="https://example.com/video.mp4", id_product=product.product_id)
    db.session.add(video)
    db.session.commit()

    assert video.video_id is not None
    assert video.video_uri == "https://example.com/video.mp4"
    assert video.id_product == product.product_id

    db.session.delete(video)
    db.session.delete(product)
    db.session.delete(developer)
    db.session.delete(user)
    db.session.commit()


def test_load_user(app_context):
    """Проверка загрузчика пользователя load_user"""
    user = User.query.get(5005)
    if not user:
        user = User(user_id=5005, login="loadusertest", password="password")
        db.session.add(user)
        db.session.commit()

    loaded_user = load_user(user.user_id)
    assert loaded_user is not None
    assert loaded_user.user_id == user.user_id
    assert loaded_user.login == "loadusertest"

    db.session.delete(user)
    db.session.commit()
