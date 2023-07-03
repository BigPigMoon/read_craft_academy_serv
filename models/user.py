from datetime import datetime

from peewee import *

from models.db import BaseModel


class User(BaseModel):
    # id
    name = CharField(null=False, unique=True)
    email = CharField(null=False, unique=True)
    password_hash = CharField(null=False)
    token = CharField(null=True)
