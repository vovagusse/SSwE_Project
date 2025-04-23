from flask import render_template, redirect, request, flash, send_from_directory, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from software_shop_webapp import db, app
from software_shop_webapp.utilities.get_current_directory import *
from software_shop_webapp.utilities.mock_data import nav_tabs, user
from software_shop_webapp.models import User
from software_shop_webapp.model_queries import *


@app.route("/login/", methods=["GET", "POST"])
def login_page() -> str:
    f_login = request.form.get("login") #stands for Form Login (Login taken from the Form)
    f_password = request.form.get("password") #stands for Form Password (Password taken from the Form)
    if f_login and f_password:
        current_user: User = User.query.filter_by(login=f_login).first()            
        if current_user and check_password_hash(current_user.password, password=f_password):
            login_user(current_user)
            next_page = request.args.get("next")
            return redirect(url_for('index'))
        else:
            flash("Логин или пароль введены неправильно")
    else:
        flash("Пожалуйста, запоолните логин и пароль")
    return render_template("login/login.html", user=user)


@app.route("/logout/", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register/", methods=["GET", "POST"])
def register_page() -> str:
    f_login = request.form.get("login") #stands for Form Login (Login taken from the Form)
    f_password = request.form.get("password") #stands for Form Password (Password taken from the Form)
    f_password2 = request.form.get("password2") #stands for Form Password (Password taken from the Form)
    if request.method=="POST":
        if not (f_login or f_password or f_password2):
            flash("Пожалуйста, заполните все поля!")
        elif f_password != f_password2:
            flash("Пароли в полях не совпадают!")
        else:
            # Everything is good!!!
            hash_pwd = generate_password_hash(f_password)
            new_user = User(login=f_login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for("login_page"))
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
    p = {}
    
    p = get_product(product_id)
    # p = p.__dict__["__data__"]
    return render_template("product.html", product=p, current_user=user)


@app.route("/add_to_cart")
@login_required
def add_to_cart() -> str:
    return redirect("/")

@app.route("/account/<int:user_id>")
@login_required
def account_page(user_id: int) -> str:
    return render_template("/account/account.html")


@app.route("/cart")
@login_required
def cart() -> str:
    return redirect("/")

@app.route("/products")
def products():
    return redirect(url_for('index'))


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
    query = dict()
    query = get_products()
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


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + "?next=" + request.url)
    return response