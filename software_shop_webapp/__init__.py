from flask import Flask
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from software_shop_webapp.utilities.mock_data import *
# from software_shop_webapp.utilities.get_current_directory import *
from software_shop_webapp.utilities.my_private_key import awesome_shit


app = Flask(__name__)
app.config['SECRET_KEY'] = awesome_shit
MY_DB = 'software_shop.db'
MY_DB = str(__path__[0]) + os.path.sep + MY_DB
print(MY_DB)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{MY_DB}"
db = SQLAlchemy(app)

from software_shop_webapp import models, routes

with app.app_context():
    db.create_all()

    
# def main() -> None:
app.run(debug=True, port=8888)  

# if __name__ == "__main__":
# main()
