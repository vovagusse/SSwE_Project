from software_shop_webapp import db, login_manager
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import datetime
from typing import List
from flask_login import UserMixin


class Product(db.Model):
    __tablename__ = "product"
    
    product_id: Mapped[int] = mapped_column(primary_key=True)
    title:      Mapped[str] = mapped_column(nullable=False, default="Abajaba Pro")
    description:Mapped[str] = mapped_column(nullable=False, default="Lorem ipsum abajaba")
    price:      Mapped[int] = mapped_column(nullable=False, default=100)
    full_price: Mapped[int] = mapped_column(nullable=False, default=100)
    is_popular: Mapped[bool] = mapped_column(default=0)
    is_new:     Mapped[bool] = mapped_column(default=1)
    files:      Mapped[List["File"]] = relationship()
    images:     Mapped[List["Image"]] = relationship()
    videos:     Mapped[List["Video"]] = relationship()
    purchases:  Mapped[List["Purchased"]] = relationship()


class Cart(db.Model):
    __tablename__ = "cart"
    id_product: Mapped[int] = mapped_column(ForeignKey("product.product_id"), 
                                            nullable=False, 
                                            primary_key=True)
    id_user:    Mapped[int] = mapped_column(ForeignKey("user.user_id"), 
                                            nullable=False,
                                            primary_key=True) 
    users:      Mapped[List["User"]] = relationship()
    products:   Mapped[List["Product"]] = relationship()

class Image(db.Model):
    __tablename__ = "image"
    
    image_id:   Mapped[int] = mapped_column(primary_key=True, 
                                            nullable=False, 
                                            autoincrement=True)
    image_uri:  Mapped[str] = mapped_column(default="https://via.placeholder.com/400x300", 
                                            nullable=False)
    id_product: Mapped[int] = mapped_column(ForeignKey("product.product_id"))  


class File(db.Model):
    __tablename__ = "file"
    
    file_id:    Mapped[int] = mapped_column(primary_key=True, 
                                            nullable=False, 
                                            autoincrement=True)
    file_uri:   Mapped[str] = mapped_column(default="D:\\\\files\\Program.7z",
                                            nullable=False)
    id_product: Mapped[int] = mapped_column(ForeignKey("product.product_id")) 


class Video(db.Model):
    __tablename__ = "video"
    
    video_id:   Mapped[int] = mapped_column(primary_key=True, 
                                            nullable=False,
                                            autoincrement=True)
    video_uri:  Mapped[str] = mapped_column(default="https://via.placeholder.com/400x300", 
                                            nullable=False)
    id_product: Mapped[int] = mapped_column(ForeignKey("product.product_id")) 


class User(db.Model, UserMixin):
    __tablename__ = "user"
    
    user_id:   Mapped[int] = mapped_column(primary_key=True, 
                                           nullable=False, 
                                           autoincrement=True)
    login:     Mapped[str] = mapped_column(unique=True, nullable=False) #Логин
    password:  Mapped[str] = mapped_column(nullable=False) #Пароль
    #Остальные данные
    full_name: Mapped[str] = mapped_column(nullable=True) #Полное ФИО
    username:  Mapped[str] = mapped_column(nullable=True) #Псевдоним или отображаемое другим пользователям имя
    def get_id(self):
        return self.user_id


class Developer(db.Model):
    __tablename__ = "developer"
    
    developer_id: Mapped[int] = mapped_column(primary_key=True, 
                                              nullable=False, 
                                              autoincrement=True)
    id_user:      Mapped[int] = mapped_column(ForeignKey("user.user_id"), 
                                              nullable=False) 


class Purchased(db.Model):
    __tablename__ = "purchased"
    
    purchase_id: Mapped[int] = mapped_column(primary_key=True)
    id_user:     Mapped[int] = mapped_column(ForeignKey("user.user_id"), 
                                             nullable=False) 
    id_product:  Mapped[int] = mapped_column(ForeignKey("product.product_id"), 
                                             nullable=False) 
    time_of_purchase: Mapped[datetime.datetime] = mapped_column(
        default=lambda: datetime.datetime.now()
    )
    cost_of_purchase: Mapped[float] = mapped_column(nullable=False)


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)