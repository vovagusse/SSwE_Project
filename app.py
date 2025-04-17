import sqlite3
from flask import Flask, render_template, redirect, request, flash, send_from_directory
from werkzeug.exceptions import abort
import os
import sys
from pprint import pprint
# from docx import Document
import datetime
from datetime import date
from peewee import *
import peewee as pw
from utilities.get_current_directory import *
from utilities.mock_data import *


from utilities.my_private_key import awesome_shit
"""This is the Flask web-server/application"""
app = Flask(__name__)
app.config['SECRET_KEY'] = awesome_shit
MY_DB = 'software_shop.db'
MY_DB = get_current_directory() + os.path.sep + MY_DB
db = SqliteDatabase(MY_DB)

# =====================================================
#                      SELECTS
# =====================================================
def get_products() -> list[dict]:
    return Product.select().dicts()
def get_product(id: int):
    return Product.get_by_id(id)


@app.route("/login/")
def login():
    return render_template("login/login.html", current_user=user)


@app.route("/register/")
def register():
    return render_template("login/register.html", current_user=user)


@app.route("/product/<int:product_id>")
def product(product_id: int):
    """Returns a web page with information about a product.

    :param product_id: primary key of product in database
    :type product_id: int
    :return: string web page that was generated using Flask and Jinja
    :rtype: str
    """
    p = get_product(product_id)
    p = p.__dict__["__data__"]
    pprint(p)
    return render_template("product.html", product=p, current_user=user)


@app.route("/add_to_cart")
def add_to_cart():
    return redirect("/")


@app.route("/cart")
def cart():
    return redirect("/")


@app.route('/')
def index():
    query = Product.select().dicts()
    return render_template("index.html", nav_tabs=nav_tabs, products=query)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def main() -> None:
    app.run(debug=True, port=8888)  


if __name__ == "__main__":
    main()


'''=========================================
ER MODEL
============================================
'''


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
    