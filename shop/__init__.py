from flask import Flask
from flask_migrate import Migrate

from shop.config import Config
from shop.models import db


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

# Имортируем представление
from shop.views import *
