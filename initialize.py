import toml
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_admin import Admin
from flask_basicauth import BasicAuth
from flask_jwt_extended import JWTManager

config = toml.load('config.toml')
app = Flask(config.get("app_name", __name__))

# APP CONFIGS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    os.path.abspath(os.path.dirname(__file__)), *config.get("database").get("path"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(*config.get("file").get("path"))
app.config.update(config.get('app_configs'))

# APP EXTENSIONS
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)
admin = Admin(app, name=config.get("app_name", __name__), template_mode='bootstrap3')
basic_auth = BasicAuth(app)
jwt = JWTManager(app)
