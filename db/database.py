import toml
import os
from flask_sqlalchemy import SQLAlchemy

config = toml.load('./config.toml').get('database')

class Database:
    def __init__(self, app):
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), *config.get("path"))
        self.db = SQLAlchemy(app)

    def get_db(self):
        return self.db