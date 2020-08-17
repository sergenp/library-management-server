import toml
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api

config = toml.load('./config.toml')
app = Flask(config.get("app_name", __name__))

# APP CONFIGS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    os.path.abspath(os.path.dirname(__file__)), *config.get("database").get("path"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_configs = config.get('app_configs')
app.config['UPLOAD_FOLDER'] = os.path.join(*config.get("file").get("path"))
app.config['BUNDLE_ERRORS'] = app_configs.get("bundle_errors")
app.config['SECRET_KEY'] = app_configs.get("secret_key")
app.config['DEBUG_MODE'] = app_configs.get("debug_mode")
app.config['PORT'] = app_configs.get("port")
# APP EXTENSIONS
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)
