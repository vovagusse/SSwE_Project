from flask import render_template, redirect, request, flash, send_from_directory, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from software_shop_webapp import db, app
from software_shop_webapp.utilities.get_current_directory import *
from software_shop_webapp.utilities.mock_data import nav_tabs
from software_shop_webapp.models import User
from software_shop_webapp.model_queries import *
import flask


@app.route("/login/", methods=["GET", "POST"])
def login_page() -> str:
    """Страница авторизации пользователя.

    :return: Веб-страница авторизации
    :rtype: str
    """
    f_login = request.form.get("login") #stands for Form Login (Login taken from the Form)
    f_password = request.form.get("password") #stands for Form Password (Password taken from the Form)
    if (request.method == "POST"):
        if f_login and f_password:
            f_user: User = User.query.filter_by(login=f_login).first()            
            if f_user and check_password_hash(f_user.password, password=f_password):
                login_user(f_user)
                next_page = request.args.get("next")
                # if (next_page == "add_to_cart"):
                #     prod_id = request.args.get("product_id")
                #     return redirect(url_for(next_page, product_id=prod_id))
                if (next_page):
                    return redirect(next_page)
                return redirect(url_for('index'))
            else:
                flash("Логин или пароль введены неправильно")
        else:
            flash("Пожалуйста, заполните логин и пароль")
    return render_template("login/login.html")


@app.route("/logout/", methods=["GET", "POST"])
@login_required
def logout():
    """Производит выход из аккаунта для текушего
    пользователя и перенаправляет на домашнюю страницу

    :return: вызов функции ``redirect(url_for("index"))``
    :rtype: Response
    """
    logout_user()
    return redirect(url_for("index"))


@app.route("/account/")
@login_required
def account():
    return render_template("account/account.html", current_user=current_user)


@app.route("/account_settings/", methods=("GET", "POST", "DELETE"))
@login_required
def account_settings():
    """Позволяет поменять данные на аккаунте, а именно:
    * Поменять отображаемое имя пользователя
    * Поменять ФИО пользователя
    * Поменять пароль аккаунта
    * Удалить аккаунт

    :return: Возвращает либо страницу ``account_settings.html`` в случае захода на страницу или ошибки при выполнении функции, либо перенаправляет на страницу ``account.html``
    :rtype: str | Response
    """
    if request.method == 'POST':
        if 'delete_account' in request.form:
            db.session.delete(current_user)
            db.session.commit()
            logout_user()  # Выходим из системы
            flash('Ваш аккаунт успешно удален', 'success')
            return redirect(url_for('index'))
        elif 'edit_profile' in request.form:
            # Получаем данные из формы
            full_name = request.form.get('full_name', '').strip()
            username = request.form.get('username', '').strip()
            
            # Словарь для хранения ошибок
            form_errors = {}
            
            # Валидация полей
            if not full_name:
                form_errors['full_name'] = 'Полное имя не может быть пустым'
            elif len(full_name) > 100:
                form_errors['full_name'] = 'Полное имя не может быть длиннее 100 символов'
                
            if not username:
                form_errors['login'] = 'Имя пользователя не может быть пустым'
            elif len(username) > 50:
                form_errors['login'] = 'Имя пользователя не может быть длиннее 50 символов'
                
            # Проверка уникальности имени пользователя
            if username and username != current_user.username:
                if User.query.filter_by(username=username).first():
                    form_errors['username'] = 'Это имя пользователя уже занято'
            
            # Если есть ошибки, передаем их в шаблон
            if form_errors:
                return render_template("account/account_settings.html", 
                                    current_user=current_user, 
                                    form_errors=form_errors,
                                    message=None)
            
            # Обновляем данные пользователя
            current_user.full_name = full_name
            current_user.username = username
            db.session.commit()
            
            # Флеш-сообщение об успехе
            flash('Профиль успешно обновлен', 'success')
            return redirect(url_for('account'))  
        elif 'change_password' in request.form:
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if not check_password_hash(current_user.password, old_password):
                flash('Неверный текущий пароль', 'error')
                return render_template('account/account_settings.html', 
                                     form_errors={},
                                     message=None)
            
            if new_password != confirm_password:
                flash('Новые пароли не совпадают', 'error')
                return render_template('account/account_settings.html', 
                                     form_errors={},
                                     message=None)
            
            current_user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Пароль успешно изменен', 'success')
            return redirect(url_for('account', user_id=current_user.user_id))
    # GET запрос - просто показываем форму    
    return render_template("account/account_settings.html", 
                           current_user=current_user, 
                           form_errors={}, 
                           message=None)


@app.route("/register/", methods=["GET", "POST"])
def register_page() -> str:
    """Обрабатывает форму регистрации нового 
    аккаунта и создаёт новую учётную запись.

    :return: при ошибке или первом посещении страницы возвращает на ``register.html`` или перенаправляет на страницу входа ``login.html``
    :rtype: str | Response
    """
    f_login = request.form.get("login") #stands for Form Login (Login taken from the Form)
    f_password = request.form.get("password") #stands for Form Password (Password taken from the Form)
    f_password2 = request.form.get("password2") #stands for Form Password (Password taken from the Form)
    f_fullname = request.form.get("full_name") #stands for Form Password (Password taken from the Form)
    f_username = request.form.get("username") #stands for Form Password (Password taken from the Form)
    if request.method=="POST":
        if not (f_login or f_password or f_password2):
            flash("Пожалуйста, заполните все поля!")
        elif f_password != f_password2:
            flash("Пароли в полях не совпадают!")
        else:
            # Everything is good!!!
            hash_pwd = generate_password_hash(f_password)
            new_user = User(login=f_login,
                            password=hash_pwd, 
                            full_name=f_fullname,
                            username=f_username)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for("login_page"))
    return render_template("login/register.html", current_user=current_user)


@app.route("/product/<int:product_id>")
def product(product_id: int) -> str:
    """Генерирует веб-страницу с продуктом на основе 
    его первичного целочисленного ключа ``product_id``. 
    Возвращает собранную на основе шаблона
    страничку при помощи Jinja.

    :param product_id: первичный ключ программного продукта в базе данных
    :type product_id: int
    :return: веб-страница
    :rtype: str
    """
    p = get_product(product_id)
    return render_template("product.html", product=p, current_user=current_user)


@app.route("/add_to_cart", methods=["GET", "POST"])
@login_required
def add_to_cart() -> str:
    """Данная функция обрабатывает операцию добавления товара в корзину. 
    Требует авторизации. В URL такой страницы присутствует параметр 
    next, который хранит страницу, куда нужно перенаправить после этой 
    операции, а также содержит аргумент ``product_id``, который содержит 
    идентификатор товара, который нужно добавить в корзину.

    :return: веб-страница в формате HTML
    :rtype: str
    """
    product_id: int = request.args.get('product_id', None)   
    next = request.args.get('next', None)
    if request.method == "POST":
        add_product_to_cart(
            user_id=current_user.user_id,
            product_id=product_id)
    if next:
        return redirect(url_for(next))
    return redirect(url_for("cart"))


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart() -> str:
    """Веб-странциа корзины. Позволяет как посмотреть товары, так и 
    удалить их из корзины.

    :return: веб-страница корзины
    :rtype: str
    """
    products = get_products_in_cart(current_user.user_id)
    fix_price = lambda x: int(x.replace(",", ""))
    summa = sum(fix_price(i.price) for i in products)
    full_summa = sum(fix_price(i.full_price) for i in products)
    if request.method == "POST":
        action = request.form.get("action")
        if action == "clear_cart":
            delete_all_products_from_cart(current_user.user_id)
            return redirect(url_for("cart"))
        if action == "proceed_purchase":
            print("\n (!) [proceed_purchase] button clicked\n")
            return redirect(url_for("checkout"))
        
    return render_template("shopping_cart/cart.html", products=products, summa=summa, full_summa=full_summa)



@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    """Веб-страница оплаты заказа. Нужна для непосредственно оплаты всего заказа.
    """
    products = get_products_in_cart(current_user.user_id)
    fix_price = lambda x: int(x.replace(",", ""))
    summa = sum(fix_price(i.price) for i in products)
    full_summa = sum(fix_price(i.full_price) for i in products)
    if request.method == "POST":
        action = request.form.get("action")
        if action == "go_back":
            return redirect(url_for("cart"))
        if action == "pay":
            print("\n (!) [pay] button clicked\n")
            # return redirect(url_for("checkout"))
    return render_template("/shopping_cart/checkout.html", products=products, summa=summa, full_summa=full_summa)


@app.route("/delete_from_cart", methods=["DELETE", "POST"])
@login_required
def delete_from_cart() -> flask.Response:
    """Данный URL соответствует удалению товара из корзины с 
    аргументом ``product_id``.

    :return: Ответ от сервера приложений Flask
    :rtype: flask.Response
    """
    # products = get_products_in_cart(current_user.user_id)
    if request.method == "POST":
        prod_id = request.args.get('product_id')
        delete_product_from_cart(product_id=prod_id, user_id=current_user.user_id)
    return redirect(url_for("cart"))


@app.route("/products")
def products() -> flask.Response:
    """Перенаправляет на основную страницу сайта (``index``).
    """
    return redirect(url_for('index'))


@app.route('/', methods=['POST', 'GET'])
def index() -> str:
    """Домашняя страница сайта. 
    На ней отрисовывается список доступных
    на текущий момент продуктов и
    пользовательские опции, по типу входа,
    регистрации, выбора продукта, и др.

    :return: веб-страница в формате HTML
    :rtype: str
    """    
    query = get_products()
    return render_template("index.html", 
                           nav_tabs=nav_tabs, 
                           products=query, 
                           current_user=current_user)


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
    """Перенаправляет на страницу входа в аккаунт, при
    этом сохраняя ту страницу, на которую пользователь 
    должен был попасть, если бы пользователь вошёл до этого.

    :param response: хранит в себе код статуса и ответ от сервера.
    :type response: ???
    :return: перенаправляет на страницу ``login.html`` либо просто показывает ответ
    :rtype: Response | ??? 
    """
    if response.status_code == 401:
        return redirect(url_for('login_page') + "?next=" + request.url)
    return response
