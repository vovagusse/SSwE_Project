from flask import Flask
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from software_shop_webapp.utilities.mock_data import *
from software_shop_webapp.utilities.my_private_key import awesome_shit
from flask_login import LoginManager


app = Flask(__name__) #: Данная переменная содержит непосредственно веб-приложение
app.config['SECRET_KEY'] = awesome_shit #: В этой строчке задаётся приватный ключ для шифрования паролей
MY_DB = 'software_shop.db'
MY_DB = str(__path__[0]) + os.path.sep + MY_DB
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{MY_DB}" #: В этой строчке задаётся название базы данных и тип подключения - SQLite
db = SQLAlchemy(app) #: В этой переменой создаётся подключение к БД с помощью SQLAlchemy
login_manager = LoginManager(app) #: В этой строчке создаётся объект LoginManager для работы с авторизации


from software_shop_webapp import models, routes
from software_shop_webapp.models import User


with app.app_context(): 
    db.create_all() #: В этой строке создаются все таблицы


app.run(debug=True, port=8888)  
