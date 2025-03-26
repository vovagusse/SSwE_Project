import sqlite3
from flask import Flask, render_template, redirect, request, flash, send_from_directory
from werkzeug.exceptions import abort
import os
import sys
from pprint import pprint
# from docx import Document
import datetime

user = {
    "name":"admin",
    "is_authenticated":0
}
nav_tabs = (
        {
            "status":1,
            "tab_name":"Все программы",
            "id":"all"
        },
        {
            "status":0,
            "tab_name":"Популярные",
            "id":"popular"
        },
        {
            "status":0,
            "tab_name":"Новые поступления",
            "id":"new"
        },
        {
            "status":0,
            "tab_name":"Скидки",
            "id":"on_sale"
        },
    )
products = (
        {
            "product_id":1,
            "image":"https://via.placeholder.com/400x300",
            "title":"Krita Pro",
            "description":"Графический редактор, позволяющий воплотить художественные мечты в жизнь.",
            "price":"2,990",
            "full_price":"2,990",
            "is_popular":1,
            "is_new":1,
            "is_on_sale":0
        },
        {
            "product_id":2,
            "image":"https://via.placeholder.com/400x300",
            "title":"Inspire Pro",
            "description":"Фоторедактор для изображений с большим количеством он-лайн шаблонов, шрифтов и кистей для создания профессиональных изображений",
            "price":"2,990",
            "full_price":"2,990",
            "is_popular":1,
            "is_new":0,
            "is_on_sale":0
        },
        {
            "product_id":3,
            "image":"https://via.placeholder.com/400x300",
            "title":"Muse Studio 2025 Professional",
            "description":"DAW для реальных профессионалов со встроенными инструментами и эффектами",
            "price":"2,990",
            "full_price":"5,990",
            "is_popular":1,
            "is_new":1,
            "is_on_sale":1
        },
        {
            "product_id":4,
            "image":"https://via.placeholder.com/400x300",
            "title":"LibreOffice Commercial Edition",
            "description":"Коммерческая лицензия на использование LibreOffice",
            "price":"2,990",
            "full_price":"2,990",
            "is_popular":0,
            "is_new":0,
            "is_on_sale":0
        },
        {
            "product_id":5,
            "image":"https://via.placeholder.com/400x300",
            "title":"Greeva",
            "description":"Онлайн-доска для планирования и отслеживания выполнения задач в компании.",
            "price":"2,990",
            "full_price":"2,990",
            "is_popular":0,
            "is_new":1,
            "is_on_sale":0
        },
        {
            "product_id":6,
            "image":"https://via.placeholder.com/400x300",
            "title":"Epic VPN",
            "description":"VPN-сервис для корпоративного сектора",
            "price":"2,990",
            "full_price":"2,990",
            "is_popular":1,
            "is_new":1,
            "is_on_sale":0
        },
        {
            "product_id":7,
            "image":"https://via.placeholder.com/400x300",
            "title":"Epic VPN Pro",
            "description":"Профессиональная версия VPN-сервиса для корпоративного сектора",
            "price":"5,999",
            "full_price":"10,990",
            "is_popular":1,
            "is_new":1,
            "is_on_sale":0
        },
    )
    


def get_current_directory():
    p = os.path.dirname(sys.argv[0])
    plat = sys.platform
    if ("win" in plat):
        p = p[0].upper() + p[1:]
        print(os.pathsep)
        p = p.replace("/", "\\")
    return p

from utilities.my_private_key import awesome_shit
"""This is the Flask web-server/application"""
app = Flask(__name__)
app.config['SECRET_KEY'] = awesome_shit
MY_DB = 'database1.db'
MY_DB = get_current_directory() + os.path.sep + MY_DB


def get_db_connection():
    conn = sqlite3.connect(MY_DB)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/login/")
def login():
    return render_template("login/login.html", current_user=user)


def search_in_products(product_id):
    for prod in products:
        if prod["product_id"] == product_id:
            return prod

@app.route("/register/")
def register():
    return render_template("login/register.html", current_user=user)


@app.route("/product/<int:product_id>")
def product(product_id: int):
    prod = search_in_products(product_id)
    return render_template("product.html", product=prod, current_user=user)


@app.route("/add_to_cart")
def add_to_cart():
    return redirect("/")


@app.route("/cart")
def cart():
    return redirect("/")


@app.route('/')
def index():
    # fake data (not by query from db)
    return render_template("index.html", nav_tabs=nav_tabs, products=products)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def main() -> None:
    # d = get_current_directory()
    # print()
    # print(f"Current directory: {d}")
    # print(MY_DB)
    app.run(debug=True, port=8888)  


if __name__ == "__main__":
    main()
