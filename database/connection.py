from peewee import Model, SqliteDatabase, CharField
from os import path

ROOT = path.dirname(path.realpath(__file__))

db = SqliteDatabase(path.join(ROOT, "vector.db"))

class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)

    class Meta:
        database = db

class Vector(Model):
    text = CharField(unique=True)
    vector = CharField(unique=True)

    class Meta:
        database = db