from .db import database
from .user import User


def database_create():
    with database:
        database.create_tables([
            User,
        ])
