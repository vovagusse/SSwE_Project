from flask import render_template, redirect, request, flash, send_from_directory
from werkzeug.exceptions import abort
from utilities.get_current_directory import *
from utilities.mock_data import *
from software_shop_webapp import db, app
from utilities.mock_data import *

@app.route("/login/")
def login() -> str:
    return render_template("login/login.html", current_user=user)


@app.route("/register/")
def register() -> str:
    return render_template("login/register.html", current_user=user)


@app.route("/product/<int:product_id>")
def product(product_id: int) -> str:
    """Генерирует веб-страницу с продуктом на основе 
    его первичного целочисленного ключа id. 
    Возвращает собранную на основе шаблона
    страничку при помощи Jinja.

    :param product_id: первичный ключ программного продукта в базе данных
    :type product_id: int
    :return: веб-страница
    :rtype: str
    """
    # p = get_product(product_id)
    # p = p.__dict__["__data__"]
    p = {}
    return render_template("product.html", product=p, current_user=user)


@app.route("/add_to_cart")
def add_to_cart() -> str:
    return redirect("/")


@app.route("/cart")
def cart() -> str:
    return redirect("/")


@app.route('/')
def index() -> str:
    """Домашняя страница сайта. 
    На ней отрисовывается список доступных
    на текущий момент продуктов и
    пользовательские опции, по типу входа,
    регистрации, выбора продукта, и др.

    :return: веб-страница в формате HTML
    :rtype: str
    """
    # query = Product.select().dicts()
    query = dict()
    return render_template("index.html", nav_tabs=nav_tabs, products=query)


@app.errorhandler(404)
def page_not_found(e):
    """Данная функция вызывается в случае, если 
    данной страницы не существует. Возвращает HTML-
    разметку страницы, где пользователю будет написано, что
    такой страницы не существует.

    :param e: ошибка, которая возникает
    :type e: _type_
    :return: веб-страница с информацией об ошибке
    :rtype: tuple(str, int)
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Данная функция вызывается в случае, если
    что-то непонятное случилось с сервером.

    :param e: ошибка, которая возникает
    :type e: _type_
    :return: веб-страница с информацией об ошибке
    :rtype: tuple(str, int)
    """
    return "Внутренняя неизвестная ошибка сервера.", 500
