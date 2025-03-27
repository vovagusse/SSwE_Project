import sqlite3
import os
import sys
from pprint import pprint
import datetime
from datetime import date
from peewee import *
import peewee as pw
from utilities.get_current_directory import *
from er_model_sqlite import *
from utilities.mock_data import *


Product.drop_table()
Image.drop_table()
Product.create_table()
Image.create_table()
with db.atomic():
    i = 1
    for p in products:
        Product.create(**p)
        Image.insert(id_product=i,
                     image_uri=p['image']
                     ).execute()
        i+=1