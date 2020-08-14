import toml
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

config = toml.load('./config.toml')
app = Flask(config.get("app_name", __name__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    os.path.abspath(os.path.dirname(__file__)), *config.get("database").get("path"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
