from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from software_shop_webapp.models import *
from software_shop_webapp import db
import pprint




def get_products() -> list[Product]:
    q = Product.query.all()
    return q

def get_developer_names_for_product(products: List[Product]) -> dict[int, str]:
    developers = dict()
    if products == None:
        return None
    for product in products:
        p_id = product.product_id
        dev_id = product.id_developer
        developers[p_id] = get_developer(dev_id).developer_name
    return developers

def get_developers_for_product(products: List[Product]) -> dict[int, Developer]:
    developers = dict()
    if products == None:
        return None
    for product in products:
        p_id = product.product_id
        dev_id = product.id_developer
        developers[p_id] = get_developer(dev_id)
    return developers


def get_first_image_for_product(products: List[Product]) -> dict[int, Image]:
    images = dict()
    if products == None:
        return None
    for product in products:
        p_id = product.product_id
        img = get_images(p_id)
        if img:
            images[p_id] = img[0]
            continue
        images[p_id] = None
    return images

def get_product(product_id: int) -> Product:
    q = Product.query.get({"product_id": product_id})
    return q

def get_developer(user_id: int) -> Developer:
    q = Developer.query.select_from(
        Developer
    ).where(
        Developer.id_user == user_id
    ).first()
    return q

def get_developer_by_id(developer_id: int) -> Developer:
    q = Developer.query.get(developer_id)
    return q

def add_developer(user_id: int, developer_name: str):
    try:
        Developer.id_user
        Developer.developer_id
        Developer.developer_name
        q = insert(
                Developer
            ).values(
                id_user=user_id,
                developer_name=developer_name
            )
        db.session.execute(q)
        db.session.commit()
    except IntegrityError:
        print(":(")

def get_products_in_cart(user_id: int) -> list[Product]:
    a = Product.query.select_from(
            Product
        ).join(
            Cart, Product.product_id == Cart.id_product
        ).where(
            Cart.id_user == user_id
        ).all()
    return a

def get_products_by_developer(developer_id: int) -> list[Product]:
    a = Product.query.select_from(
            Product
        ).where(
            Product.id_developer == developer_id
        ).all()
    return a

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

def add_products_to_purchased(
        user_id: int, 
        products: List[Product], 
        order_id: int
    ) -> None:
    if not get_order(order_id):
        return
    try:    
        purchased = get_purchased_products(user_id)
        values = []
        summa = 0
        for product in products:
            if product in purchased:
                continue
            purchase_dict = {}
            purchase_dict['id_user'] = user_id
            purchase_dict['id_product'] = product.product_id
            price = product.price
            price = price.replace(",", "")
            price=int(price)
            print(price)
            purchase_dict['cost_of_purchase'] = price
            purchase_dict['id_order']=order_id
            values.append(purchase_dict)
            summa += price
        q = insert(
                Purchased
            ).values(
                values
            )
        print(q)
        db.session.execute(q)
        db.session.commit()
    except IntegrityError:
        print("integrity error on add_products_to_purchased() :(")

def delete_product_from_cart(user_id: int, product_id: int) -> None:
    q = delete(
            Cart
        ).where(
            Cart.id_product==product_id,
            Cart.id_user==user_id
        )
    db.session.execute(q)
    db.session.commit()

def delete_all_products_from_cart(user_id: int) -> None:
    q = delete(
            Cart
        ).where(
            Cart.id_user==user_id
        )
    db.session.execute(q)
    db.session.commit()
    
# Заказы и прочее

def get_orders() -> list[Order]:
    q = Order.query.all()
    return q

def get_order(order_id: int) -> Order:
    a = Order.query.select_from(
            Order
        ).where(
            Order.order_id == order_id
        ).first()
    return a

def delete_order(order_id: int) -> None:
    q = delete(
            Order
        ).where(
            Order.order_id == order_id
        )
    db.session.execute(q)
    db.session.commit()


def delete_order_and_purchased(order_id: int) -> None:
    # Удаляем связанные записи в Purchased
    purchased = Purchased.query.filter_by(id_order=order_id).first()
    if purchased:
        db.session.delete(purchased)
    
    # Удаляем сам заказ
    order = Order.query.get(order_id)
    if order:
        db.session.delete(order)
    
    db.session.commit()


# initial state = pending
def create_order(
        user_id: int,
        amount: float
    ) -> Order:
    order = Order(
        id_user=user_id,
        amount=amount,
        status="pending"
    )
    db.session.add(order)
    db.session.commit()
    return order

# card number is assumed correct
def process_order(card_number: str, order_id: int):
    ord = get_order(order_id)
    ord.card_number = card_number
    ord.status = 'success'
    db.session.commit()

# returns all producs user has purchased
def get_purchased_products(user_id: int) -> List[Product]:
    a = Product.query.select_from(
            Product
        ).join(
            Purchased, Product.product_id == Purchased.id_product
        ).where(
            Purchased.id_user == user_id
        ).all()
    return a



# Файлы, видео и фото

# 1) Файлы

def add_file(file_uri: str, product_id: int):
    try:
        q = insert(
                File
            ).values(
                id_product=product_id,
                file_uri=file_uri
            )
        db.session.execute(q)
        db.session.commit()
    except IntegrityError:
        print(":(")

def delete_file_by_uri(file_uri_arg: str, product_id_arg: int):
    try:
        q = File.__table__.delete().where(
            File.file_uri == file_uri_arg, 
            File.id_product == product_id_arg
        )
        db.session.execute(q)
        db.session.commit()
    except:
        print("could not delete file idk why sorry brother")

def get_files(product_id: int) -> List[File]:
    q = File.query.select_from(
            File
        ).join(
            Product, product_id == File.id_product
        ).all()
    return q

def get_file(file_id: int) -> File:
    q = File.query.get({"file_id":file_id})
    return q


# 2) Изображения

def add_image(image_uri: str, product_id: int):
    q = insert(
            Image
        ).values(
            id_product=product_id,
            image_uri=image_uri
        )
    print(q)
    try:
        db.session.execute(q)
        db.session.commit()
    except IntegrityError:
        print(":(")

def delete_image_by_uri(image_uri_arg: str, product_id_arg: int):
    try:
        q = Image.__table__.delete().where(
            Image.image_uri == image_uri_arg, 
            Image.id_product == product_id_arg
        )
        db.session.execute(q)
        db.session.commit()
    except:
        print("could not delete file idk why sorry brother")

def get_images(product_id: int) -> List[Image]:
    q = Image.query.select_from(
            Image
        ).join(
            Product, product_id == Image.id_product
        ).all()
    return q

def get_image(image_id: int) -> Image:
    q = Image.query.get({"image_id":image_id})
    return q



# 3) Видео

def add_video(video_uri: str, product_id: int):
    try:
        q = insert(
                Video
            ).values(
                id_product=product_id,
                video_uri=video_uri
            )
        db.session.execute(q)
        db.session.commit()
    except IntegrityError:
        print(":(")

def delete_video_by_uri(video_uri_arg: str, product_id_arg: int):
    try:
        q = Video.__table__.delete().where(
            Video.video_uri == video_uri_arg, 
            Video.id_product == product_id_arg
        )
        db.session.execute(q)
        db.session.commit()
    except:
        print("could not delete file idk why sorry brother")

def get_videos(product_id: int) -> List[Video]:
    q = Video.query.select_from(
            Video
        ).join(
            Product, product_id == Video.id_product
        ).all()
    return q

def get_video(video_id: int) -> Video:
    q = Video.query.get({"video_id":video_id})
    return q


