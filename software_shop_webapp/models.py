from software_shop_webapp import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import datetime
from typing import List


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


class User(db.Model):
    __tablename__ = "user"
    
    user_id:   Mapped[int] = mapped_column(primary_key=True, 
                                           nullable=False, 
                                           autoincrement=True)
    full_name: Mapped[str] = mapped_column(nullable=False) #Полное ФИО
    username:  Mapped[str] = mapped_column() #Псевдоним или отображаемое другим пользователям имя
    mail:      Mapped[str] = mapped_column(nullable=False) #Адрес почты (Логин)
    password:  Mapped[str] = mapped_column(nullable=False) #Пароль


class Developer(db.Model):
    __tablename__ = "developer"
    
    developer_id: Mapped[int] = mapped_column(primary_key=True, 
                                              nullable=False, 
                                              autoincrement=True)
    id_user:      Mapped[int] = mapped_column(ForeignKey("user.user_id"), 
                                              nullable=False) 


class AuthSession(db.Model):
    __tablename__ = "authsession"
    
    auth_id: Mapped[int] = mapped_column(primary_key=True, 
                                         nullable=False, 
                                         autoincrement=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("user.user_id"), 
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
