from peewee import SqliteDatabase, Model


database = SqliteDatabase('read_craft.db')


class BaseModel(Model):
    class Meta:
        database = database
