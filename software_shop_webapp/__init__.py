from flask import Flask
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from software_shop_webapp.utilities.mock_data import *
from software_shop_webapp.utilities.my_private_key import awesome_shit
from flask_login import LoginManager

ALLOWED_FILE_EXTENSIONS = {"txt", "pdf", 'zip', 'rar', '7z', 'tar'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mkv'}

app = Flask(__name__) #: Данная переменная содержит непосредственно веб-приложение
app.config['SECRET_KEY'] = awesome_shit #: В этой строчке задаётся приватный ключ для шифрования паролей
MY_DB = 'software_shop.db'
MY_DB = str(__path__[0]) + os.path.sep + MY_DB
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{MY_DB}" #: В этой строчке задаётся название базы данных и тип подключения - SQLite
app.config['UPLOAD_FOLDER'] = "software_shop_webapp/files"
app.config['VIDEO_UPLOAD_FOLDER'] = "software_shop_webapp/static/videos"
app.config['IMAGE_UPLOAD_FOLDER'] = "software_shop_webapp/static/images"
db = SQLAlchemy(app) #: В этой переменой создаётся подключение к БД с помощью SQLAlchemy
login_manager = LoginManager(app) #: В этой строчке создаётся объект LoginManager для работы с авторизации


from software_shop_webapp import models, routes


with app.app_context():
    # так можно удалить таблицу если она хреново придумана
    # models.Image.__table__.delete()
    # models.Product.__table__.drop(db.engine)
    # models.Video.__table__.drop(db.engine)
    db.create_all() #: В этой строке создаются все таблицы

