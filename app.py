import sqlite3
from flask import Flask, render_template, redirect, request, flash, send_from_directory
from werkzeug.exceptions import abort
import os
import sys
from pprint import pprint
# from docx import Document
import datetime


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


@app.route("/login")
def login():
    return render_template("login/login.html")


@app.route('/')
def index():
    return render_template("index.html")


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
