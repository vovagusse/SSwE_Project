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
from er_model_sqlite import *
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
