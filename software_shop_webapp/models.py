from software_shop_webapp import db
from sqlalchemy.orm import Mapped, mapped_column

class Product(db.Model):
    product_id: Mapped[int] = mapped_column(primary_key=True)
    title:      Mapped[str] = mapped_column(nullable=False, default="Abajaba Pro")
    description:Mapped[str] = mapped_column(nullable=False, default="Lorem ipsum abajaba")
    price:      Mapped[int] = mapped_column(nullable=False, default=100)
    full_price: Mapped[int] = mapped_column(nullable=False, default=100)
    is_popular: Mapped[bool] = mapped_column(default=0)
    is_new:     Mapped[bool] = mapped_column(default=1)


# class Image(db.Model):
#     image_id: Mapped[int] = mapped_column(primary_key=True)
#     image_uri: Mapped[str] = mapped_column(default="https://via.placeholder.com/400x300")
#     id_product = ForeignKeyField(
#         Product, backref="product_id") 


# class File(db.Model):
#     file_id: Mapped[int] = mapped_column(primary_key=True)
#     file_uri: Mapped[str] = mapped_column()
#     id_product = ForeignKeyField(
#         Product, backref="product_id") 


# class Video(db.Model):
#     video_id: Mapped[int] = mapped_column(primary_key=True)
#     video_uri: Mapped[str] = mapped_column(default="https://via.placeholder.com/400x300")
#     id_product = ForeignKeyField(
#         Product, backref="product_id") 


# class File(db.Model):
#     file_id: Mapped[int] = mapped_column(primary_key=True)
#     file_uri: Mapped[str] = mapped_column()
#     id_product = ForeignKeyField(
#         Product, backref="product_id") 


# class Video(db.Model):
#     video_id: Mapped[int] = mapped_column(primary_key=True)
#     video_uri: Mapped[str] = mapped_column(default="https://via.placeholder.com/400x300")
#     id_product = ForeignKeyField(
#         Product, backref="product_id") 


class User(db.Model):
    user_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column() #Полное ФИО
    username: Mapped[str] = mapped_column() #Псевдоним или отображаемое другим пользователям имя
    mail: Mapped[str] = mapped_column() #Адрес почты (Логин)
    password: Mapped[str] = mapped_column() #Пароль


# class Developer(db.Model):
#     developer_id: Mapped[int] = mapped_column(primary_key=True)
#     id_user = ForeignKeyField(
#         User, backref="user_id") 


# class AuthSession(db.Model):
#     auth_id: Mapped[int] = mapped_column(primary_key=True)
#     id_user = ForeignKeyField(
#         User, backref="user_id") 


# class Purchased(db.Model):
#     purchase_id: Mapped[int] = mapped_column(primary_key=True)
#     id_user = mapped_column(ForeignKey("user.id"))
#     ForeignKeyField(
#         User, backref="user_id")
#     id_product = ForeignKeyField(
#         Product, backref="product_id") 
#     # ugly ass fucking SQLAlchemy mapping with some datetime.datetime.now() shit cuz SQLAlchemy is ugly at times.
#     time_of_purchase: Mapped[datetime.datetime] = mapped_column(default=lambda: datetime.datetime.now())
#     cost_of_purchase: Mapped[float] = mapped_column()
