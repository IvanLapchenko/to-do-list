import os
from flask import Flask
from flask_caching import Cache
from datetime import timedelta
from .models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.getcwd())}/app.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

db.init_app(app)

with app.app_context():
    db.create_all()

from . import routes
