from flask import render_template, redirect, request, flash, send_from_directory, send_file, url_for, jsonify, Blueprint
from flask_login import login_user, login_required, logout_user, current_user, AnonymousUserMixin
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from software_shop_webapp import db, app
from software_shop_webapp.utilities.get_current_directory import *
from software_shop_webapp.utilities.mock_data import nav_tabs
from software_shop_webapp.utilities.file_check import *
from software_shop_webapp.models import User
from software_shop_webapp.model_queries import *
import flask
import time
from glob import glob
from io import BytesIO
from zipfile import ZipFile
import os


@app.template_filter('get_developer_id')
def get_developer_id_filter(var: str):
    return get_developer(current_user.user_id).developer_id


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
        if 'delete_developer_account' in request.form and current_user.is_developer:
            developer = get_developer(current_user.user_id)
            db.session.delete(developer)            
            current_user.is_developer = False
            db.session.commit()
            flash('Ваш аккаунт разработчика успешно удален', 'success')
            return redirect(url_for('account_settings'))
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
                                    message="Произошла ошибка во время смены имени пользователя")
            
            # Обновляем данные пользователя
            current_user.full_name = full_name
            current_user.username = username
            db.session.commit()
            
            # Флеш-сообщение об успехе
            flash('Профиль успешно обновлен', 'success')
            return redirect(url_for('account_settings'))  
        elif 'edit_developer_profile' in request.form and current_user.is_developer:
            # Получаем данные из формы
            dev = get_developer(current_user.user_id)
            f_developer_name = request.form.get('developer_name', '').strip()
            
            # Словарь для хранения ошибок
            form_errors = {}
            
            # Валидация полей
            if not f_developer_name:
                form_errors['developer_name'] = 'Имя разработчика не может быть пустым'
            elif len(f_developer_name) > 100:
                form_errors['developer_name'] = 'Имя разработчика не может быть длиннее 100 символов'
                
            # Проверка уникальности имени пользователя
            if f_developer_name and f_developer_name != dev.developer_name:
                if Developer.query.filter_by(developer_name=f_developer_name).first():
                    form_errors['developer_name'] = 'Это имя разработчика уже занято'
            
            # Если есть ошибки, передаем их в шаблон
            if form_errors:
                return render_template("account/account_settings.html", 
                                    current_user=current_user, 
                                    form_errors=form_errors,
                                    developer=dev,
                                    message="Произошла ошибка во время смены имени разработчика")
            
            # Обновляем данные пользователя
            dev.developer_name = f_developer_name
            db.session.commit()
            return redirect(url_for('account_settings'))  
        elif "create_developer_account" in request.form and not current_user.is_developer:
            # Получаем данные из формы
            developer_name = request.form.get('developer_name', '').strip()
            print("\n                 DEV NAME: ",developer_name, "\n")
            form_errors = {}
            if Developer.query.filter_by(developer_name=developer_name).first():
                form_errors['developer_name'] = "Это имя разрабоотчика уже занято"
            
            if form_errors: 
                return render_template("account/account_settings.html",
                                        current_user=current_user, 
                                        form_errors=form_errors,
                                        message="Произошла ошибка во время создания профиля разработчика")
            add_developer(current_user.user_id, developer_name)
            current_user.is_developer=True
            db.session.commit()
            return redirect(url_for("account_settings"))
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
            return redirect(url_for('account_settings'))
    # GET запрос - просто показываем форму    
    if current_user.is_developer:
        developer = get_developer(current_user.user_id)
        return render_template("account/account_settings.html", 
                                current_user=current_user, 
                                form_errors={}, 
                                message=None, 
                                developer=developer)

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


@app.route("/developer_profile/<int:developer_id>")
def developer_profile(developer_id: int):
    return redirect(url_for("public_developer_profile", developer_id=developer_id))

@app.route("/public_developer_profile/<int:developer_id>")
def public_developer_profile(developer_id: int):
    products = get_products_by_developer(developer_id)
    developer = get_developer_by_id(developer_id)
    return render_template("dev_account/public_developer_profile.html",
                           products=products,
                           developer=developer)


@app.route("/add_product/", methods=["POST", "GET"])
@login_required
def add_product():
    if (not current_user.is_developer):
        return redirect(url_for('index'))
    developer = get_developer(current_user.user_id)
    
    if request.method == "POST":
        button_name = request.form.get('action')
        
        title = request.form.get("title")
        description = request.form.get("description")
        price = request.form.get("price")
        full_price = request.form.get("full_price")
        developer_id = developer.developer_id
        is_new = True
        is_popular = False
        if not price:
            price = full_price
            
            
        # Валидация данных
        necessary_args = title, full_price
        not_all_args_filled = not all(necessary_args)
        not_good_price = not (price <= full_price)
        bad_title_length = len(title) > 100
        if bad_title_length or not_all_args_filled or not_good_price:
            if (bad_title_length):
                flash("Слишком длинное название!")
            if not_all_args_filled:
                flash("Не все обязательные параметры были заполнены!")
            if not_good_price:
                flash("Цена по скидке не должна превосходить цену без скидки!")
            return redirect(url_for("add_product"))
        
        if button_name == "add_file":
            print("add_file")
            product = Product(title=title,
                          description=description,
                          full_price=full_price,
                          price=price,
                          id_developer=developer_id,
                          is_new=is_new,
                          is_popular=is_popular)
            db.session.commit()
            return redirect(url_for("add_file_route", product_id=product.product_id))
        elif button_name == "add_video":
            print("add_video")
            product = Product(title=title,
                          description=description,
                          full_price=full_price,
                          price=price,
                          id_developer=developer_id,
                          is_new=is_new,
                          is_popular=is_popular)
            db.session.commit()
            return redirect(url_for("add_video_route", product_id=product.product_id))
        elif button_name == "add_image":
            print("add_image")
            product = Product(title=title,
                          description=description,
                          full_price=full_price,
                          price=price,
                          id_developer=developer_id,
                          is_new=is_new,
                          is_popular=is_popular)
            db.session.commit()
            return redirect(url_for("add_image_route", product_id=product.product_id))
        elif button_name == "save":
            print("save")
            product = Product(title=title,
                          description=description,
                          full_price=full_price,
                          price=price,
                          id_developer=developer_id,
                          is_new=is_new,
                          is_popular=is_popular)
            db.session.add(product)
            db.session.commit()
            print(product.product_id)
            return redirect(url_for("edit_product", product_id=product.product_id))
        elif button_name == "cancel":
            return redirect(url_for('index'))
    return render_template("dev_account/add_product.html",
                           developer=developer, 
                           subtitle_text="Добавление нового программного средства")


@app.route("/edit_product/<int:product_id>", methods=["POST", "GET"])
@login_required
def edit_product(product_id: int):
    if (not current_user.is_developer):
        return redirect(url_for('index'))
    product = get_product(product_id)
    developer = get_developer(current_user.user_id)
    
    if request.method == "POST":
        button_name = request.form.get('action')
        
        title = request.form.get("title")
        description = request.form.get("description")
        price = request.form.get("price")
        full_price = request.form.get("full_price")
        developer_id = developer.developer_id
        is_new = True
        is_popular = False

        # Валидация данных
        necessary_args = title, full_price
        not_all_args_filled = not all(necessary_args)
        not_good_price = not (price <= full_price)
        bad_title_length = len(title) > 100
        if bad_title_length or not_all_args_filled or not_good_price:
            if (bad_title_length):
                flash("Слишком длинное название!")
            if not_all_args_filled:
                flash("Не все обязательные параметры были заполнены!")
            if not_good_price:
                flash("Цена по скидке не должна превосходить цену без скидки!")
            # return redirect(url_for("add_product"))
            return redirect(url_for("edit_product", product_id=product.product_id))
        
        if button_name == "add_file":
            return redirect(url_for("add_file_route", product_id=product.product_id))
        elif button_name == "add_video":
            return redirect(url_for("add_video_route", product_id=product.product_id))
        elif button_name == "add_image":
            return redirect(url_for("add_image_route", product_id=product.product_id))
        elif button_name == "save":
            ineq1 = product.title != title
            ineq2 = product.description != description
            ineq3 = product.full_price != full_price
            ineq4 = product.price != price
            if (ineq1): product.title = title
            if (ineq2): product.description = description
            if (ineq3): product.full_price = full_price
            if (ineq4): product.price = price
            if any((ineq1, ineq2, ineq3, ineq4)):
                db.session.commit()
            return redirect(url_for("edit_product", product_id=product.product_id))
        elif button_name == "cancel":
            return redirect(url_for('index'))
    return render_template("dev_account/add_product.html",
                           developer=developer,
                           subtitle_text="Редактирование программного средства",
                           product=product)

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
    developer = get_developer_by_id(p.id_developer)
    return render_template("product.html", 
                           product=p,
                           developer=developer)


@app.route("/purchased/")
@login_required
def purchased() -> str:
    p = get_purchased_products(current_user.user_id)
    developers = get_developers_for_product(p)
    return render_template("account/purchased.html", 
                           purchased=p, 
                           developers=developers)


@app.route("/download/<int:product_id>", methods=["GET", "POST"])
@login_required
def download(product_id: int) -> str:
    print(product_id)
    files = get_files(product_id)
    folder = app.config['UPLOAD_FOLDER']
    archive_name = f"{get_product(product_id).title}.zip"
    stream = BytesIO()
    with ZipFile(stream, "w") as zf:
        for file in files:
            path = os.path.join(folder, file.file_uri)
            if (os.path.exists(path)):
                zf.write(path, os.path.basename(file.file_uri))
            else:
                print("File not found! Deleting from database...")
                delete_file_by_uri(file, product_id)
    stream.seek(0)
    return send_file(stream, as_attachment=True, download_name=archive_name)
            
   

@app.route('/download_file/<file_uri>', methods=("POST", "GET"))
@login_required
def download_file(file_uri: str):
    path = os.path.join(app.config['UPLOAD_FOLDER'], file_uri)
    return send_file(os.path.join("..", path), as_attachment=True)

# IMAGE_UPLOAD_FOLDER
# VIDEO_UPLOAD_FOLDER

@login_required
@app.route('/download_image/<image_uri>', methods=("POST", "GET"))
def download_image(image_uri: str):
    path = os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], image_uri)
    return send_file(os.path.join("..", path), as_attachment=True)

@login_required
@app.route('/download_video/<video_uri>', methods=("POST", "GET"))
def download_video(video_uri: str):
    path = os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], video_uri)
    return send_file(os.path.join("..", path), as_attachment=True)


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


@app.route("/delete_file/<int:file_id>", methods=["GET", "POST", "DELETE"])
@login_required
def delete_file_route(file_id: int):
    file = get_file(file_id)
    filename = file.file_uri
    folder = app.config['UPLOAD_FOLDER']
    path = os.path.join(folder, filename)
    # Удаление файлика непосредственно:
    try:
        os.remove(path)
    except:
        print("File was deleted or renamed")
    finally:
        product_id = file.id_product
        delete_file_by_uri(filename, product_id)
    return redirect(url_for('add_file_route', 
                            product_id=product_id))

@app.route("/delete_image/<int:image_id>", methods=["GET", "POST", "DELETE"])
@login_required
def delete_image_route(image_id: int):
    image = get_image(image_id)
    filename = image.image_uri
    folder = app.config['IMAGE_UPLOAD_FOLDER']
    path = os.path.join(folder, filename)
    # Удаление картинки непосредственно:
    try: 
        os.remove(path)
    except FileNotFoundError:
        print('Image was deleted or renamed')
    finally:
        product_id = image.id_product
        delete_image_by_uri(filename, product_id)
    return redirect(url_for('add_image_route', 
                            product_id=product_id))

@app.route("/delete_video/<int:video_id>", methods=["GET", "POST", "DELETE"])
@login_required
def delete_video_route(video_id: int):
    video = get_video(video_id)
    filename = video.video_uri
    folder = app.config['VIDEO_UPLOAD_FOLDER']
    path = os.path.join(folder, filename)
    # Удаление видео непосредственно:
    try: 
        os.remove(path)
    except FileNotFoundError:
        print('Video was deleted or renamed')
    finally:
        product_id = video.id_product
        delete_video_by_uri(filename, product_id)
    return redirect(url_for('add_video_route', 
                            product_id=product_id))

@app.route("/add_file/<int:product_id>", methods=["GET", "POST"])
@login_required
def add_file_route(product_id: int):
    print("\n (!) Add file page loaded\n")
    p = get_product(product_id)
    added_files = os.listdir(app.config['UPLOAD_FOLDER'])
    added_files = get_files(product_id)
    fileformats = set()
    fileformats.update(ALLOWED_FILE_EXTENSIONS)
    fileformats = ",".join("." + e for e in fileformats)
    if request.method == "POST":    
        if 'file' not in request.files:
            # flash('no file part')
            print(" (!) No actual file :(")
            return redirect(url_for('add_file_route', product_id=product_id))
        # fetch files
        files_to_upload = request.files.getlist("file")
        if not files_to_upload:
            print("no files")
        for file in files_to_upload:            
            if file.filename == '':
                print(" (!) no file selected")
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                folder = app.config['UPLOAD_FOLDER']
                file.save(os.path.join(folder, filename))
                add_file(filename, product_id)
        
        return redirect(url_for("add_file_route", product_id=product_id))

    return render_template("dev_account/add_file.html", 
                           product_id=product_id,
                           accept=fileformats,
                           files=added_files,
                           file_amount=len(added_files))

@app.route("/add_image/<int:product_id>", methods=["GET", "POST"])
@login_required
def add_image_route(product_id: int):
    print("\n (!) Add image page loaded\n")
    p = get_product(product_id)
    # added_files = os.listdir(app.config['IMAGE_UPLOAD_FOLDER'])
    added_images = get_images(product_id)
    fileformats = set()
    fileformats.update(ALLOWED_IMAGE_EXTENSIONS)
    fileformats = ",".join("." + e for e in fileformats)
    print(added_images)
    if request.method == "POST":    
        if 'file' not in request.files:
            # flash('no file part')
            print(" (!) No actual file :(")
            return redirect(url_for('add_image_route', product_id=product_id))
        # fetch files
        files_to_upload = request.files.getlist("file")
        print("Files to upload:", files_to_upload)
        if not files_to_upload:
            print("no files")
        for file in files_to_upload:            
            if file.filename == '':
                print(" (!) no file selected")
            if file and allowed_image(file.filename):
                filename = secure_filename(file.filename)
                folder = app.config['IMAGE_UPLOAD_FOLDER']
                path = os.path.join(folder, filename)
                print(path)
                file.save(path)
                add_image(filename, product_id)
        
        return redirect(url_for("add_image_route", product_id=product_id))

    return render_template("dev_account/add_image.html", 
                           product_id=product_id,
                           accept=fileformats,
                           images=added_images,
                           file_amount=len(added_images))


@app.route("/add_video/<int:product_id>", methods=["GET", "POST"])
@login_required
def add_video_route(product_id: int):
    if (current_user):
        print(current_user.is_developer)
    print("\n (!) Add video page loaded\n")
    p = get_product(product_id)
    # added_files = os.listdir(app.config['IMAGE_UPLOAD_FOLDER'])
    added_videos = get_videos(product_id)
    fileformats = set()
    fileformats.update(ALLOWED_VIDEO_EXTENSIONS)
    fileformats = ",".join("." + e for e in fileformats)
    print("\nAdded videos:", added_videos, "\n")
    if request.method == "POST":    
        if 'file' not in request.files:
            # flash('no file part')
            print(" (!) No actual file :(")
            return redirect(url_for('add_image_route', product_id=product_id))
        # fetch files
        files_to_upload = request.files.getlist("file")
        print("Files to upload:", files_to_upload)
        if not files_to_upload:
            print("no files")
        for file in files_to_upload:            
            if file.filename == '':
                print(" (!) no file selected")
            if file and allowed_video(file.filename):
                filename = secure_filename(file.filename)
                folder = app.config['VIDEO_UPLOAD_FOLDER']
                path = os.path.join(folder, filename)
                print(path)
                file.save(path)
                add_video(filename, product_id)
        
        return redirect(url_for("add_video_route", product_id=product_id))

    return render_template("dev_account/add_video.html", 
                           product_id=product_id,
                           accept=fileformats,
                           videos=added_videos,
                           file_amount=len(added_videos))


# Оплата

@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart() -> str:
    """Веб-странциа корзины. Позволяет как посмотреть товары, так и 
    удалить их из корзины.

    :return: веб-страница корзины
    :rtype: str
    """
    products = get_products_in_cart(current_user.user_id)
    developers = get_developers_for_product(products)
    summa = sum(i.price for i in products)
    full_summa = sum(i.full_price for i in products)
    if request.method == "POST":
        action = request.form.get("action")
        if action == "clear_cart":
            delete_all_products_from_cart(current_user.user_id)
            return redirect(url_for("cart"))
        if action == "proceed_purchase":
            print("\n (!) [proceed_purchase] button clicked\n")
            return redirect(url_for("checkout"))
            
    return render_template("shopping_cart/cart.html", 
                           products=products,
                           developers=developers, 
                           summa=summa,
                           full_summa=full_summa)

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    """Веб-страница оплаты заказа. Нужна для непосредственно оплаты всего заказа.
    """
    products = get_products_in_cart(current_user.user_id)
    developers = get_developers_for_product(products)
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
            o = create_order(current_user.user_id, summa)
            return redirect(url_for('payment', order_id=o.order_id))
    return render_template("/shopping_cart/checkout.html", 
                           products=products, 
                           developers=developers,
                           summa=summa, 
                           full_summa=full_summa)


@app.route('/payment', methods=["POST", "GET"])
def payment():
    products_from_cart = get_products_in_cart(current_user.user_id)
    print(products_from_cart)
    order_id = request.args.get("order_id")
    my_order = get_order(order_id)
    print(f"Order:\n        amount: {my_order.amount}\n\
        card number: {my_order.card_number}\n\
        order_id: {my_order.order_id}\n\
        order_status: {my_order.status}")
    add_products_to_purchased(current_user.user_id, 
                              products_from_cart,
                              order_id)
    if request.method == "POST":
        try:
            # Получаем данные из формы
            data = request.form
            order_id = request.args.get('order_id')
            
            # Получаем существующий заказ
            order = get_order(order_id)
            if not order:
                return render_template('payment/error.html', error='Заказ не найден')
                
            # Проверяем данные карты
            card_number = data['card_number']
            if len(card_number) != 16 or not card_number.isdigit():
                return redirect(url_for('/error', order_id=order.order_id, error='Неверный номер карты'))
                
            # Симуляция проверки карты (в реальном приложении здесь должна быть
            # интеграция с платежной системой)
            if card_number != '4242424242424242':  # Тестовая карта
                return redirect(url_for('/error', order_id=order.order_id, error='Ошибка оплаты'))
                
            # Обновляем статус заказа
            process_order(card_number, order_id)
            
            return redirect(url_for('success'))
        except Exception as e:
            flash(f"Оплата не прошла! {str(e)}")
            return redirect(url_for('error', order_id=order.order_id))
    
    return render_template('/payment/payment.html', order=my_order)


@app.route('/success')
def success():
    order_id = request.args.get("order_id")
    return render_template('payment/success.html')


@app.route('/error')
def error():
    order_id = request.args.get("order_id")
    error = request.args.get("error")
    
    return render_template('payment/error.html')

@app.route("/cancel_order")
def cancel_order():
    order_id = request.args.get("order_id")
    if not order_id:
        flash("Ошибка: заказ не найден")
        return redirect(url_for("cart"))
    
    try:
        delete_order_and_purchased(order_id)
        flash("Заказ успешно отменен")
        return redirect(url_for("cart"))
    except Exception as e:
        flash(f"Ошибка при отмене заказа: {str(e)}")
        return redirect(url_for("cart"))


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
    products = get_products()
    images = get_first_image_for_product(products)
    developers = get_developers_for_product(products)
    print(images.values())
    return render_template("index.html", 
                           nav_tabs=nav_tabs, 
                           products=products, 
                           images=images,
                           developers=developers,
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

# @app.before_request
# def anonymous_user_mixin():
#     if type(current_user) == type(AnonymousUserMixin):
#         redirect_to_signin()
