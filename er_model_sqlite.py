from peewee import *
from app import MY_DB
# from . import db
import datetime

db=SqliteDatabase(MY_DB)


class Product(Model):
    product_id = AutoField()
    title = TextField(default="Abajaba Pro")
    description = TextField(default="Lorem ipsum abajaba")
    price = IntegerField(default=100)
    full_price = IntegerField(default=100)
    is_popular = BooleanField(default=0)
    is_new = BooleanField(default=1)
    class Meta:
        database = db

class Image(Model):
    image_id = AutoField()
    image_uri = TextField(
        default="https://via.placeholder.com/400x300")
    id_product = ForeignKeyField(
        Product, backref="product_id") 
    class Meta:
        database = db

class File(Model):
    file_id = AutoField()
    file_uri = TextField()
    id_product = ForeignKeyField(
        Product, backref="product_id") 
    class Meta:
        database = db


class Video(Model):
    video_id = AutoField()
    video_uri = TextField(
        default="https://via.placeholder.com/400x300")
    id_product = ForeignKeyField(
        Product, backref="product_id") 
    class Meta:
        database = db

class File(Model):
    file_id = AutoField()
    file_uri = TextField()
    id_product = ForeignKeyField(
        Product, backref="product_id") 
    class Meta:
        database = db


class Video(Model):
    video_id = AutoField()
    video_uri = TextField(
        default="https://via.placeholder.com/400x300")
    id_product = ForeignKeyField(
        Product, backref="product_id") 
    class Meta:
        database = db


class User(Model):
    user_id = AutoField()
    full_name = TextField() #Полное ФИО
    username = TextField() #Псевдоним или отображаемое другим пользователям имя
    mail = TextField() #Адрес почты (Логин)
    password = TextField() #Пароль
    class Meta:
        database = db


class Developer(Model):
    developer_id = AutoField()
    id_user = ForeignKeyField(
        User, backref="user_id") 
    class Meta:
        database = db


class AuthSession(Model):
    auth_id = AutoField()
    id_user = ForeignKeyField(
        User, backref="user_id") 
    class Meta:
        database = db


class Purchased(Model):
    purchase_id = AutoField()
    id_user = ForeignKeyField(
        User, backref="user_id")
    id_product = ForeignKeyField(
        Product, backref="product_id") 
    time_of_purchase = DateTimeField(default=datetime.datetime.now())
    cost_of_purchase = FloatField()
    class Meta:
        database = db
    