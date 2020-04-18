from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('f1.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)

class Session(BaseModel):
    user = ForeignKeyField(User, related_name='sessions')
    title = TextField()
    track = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)

class Record(BaseModel):
    session = ForeignKeyField(Session, related_name='records')
    rpm = TextField()
    throttle = TextField()
    brake = TextField()
    speed = TextField()
    gear = TextField()


db.connect()
db.create_tables([User, Session, Record], safe=True)

# db test data and static session
rebuild = False
if rebuild == True:
    ryan = User.create(username='ryan')