from peewee import *
from app import MY_DB


db=SqliteDatabase(MY_DB)


class Product(Model):
    product_id = AutoField()
    title = TextField(default="Abajaba Pro")
    description = TextField(default="Lorem ipsum abajaba")
    price = IntegerField(default=100)
    full_price = IntegerField(default=100)
    is_popular = BooleanField(default=0)
    is_new = BooleanField(default=1)
    class Meta:
        database = db

class Image(Model):
    image_id = AutoField()
    image_uri = TextField(
        default="https://via.placeholder.com/400x300")
    #primary key of of product is product_id
    id_product = ForeignKeyField(
        Product, backref="product_id") 
    class Meta:
        database = db
