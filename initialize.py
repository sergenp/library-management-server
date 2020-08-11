import os
from db.database import Database
from api.Api import API
from api.Resources import HelloWorld
from flask import Flask
import toml

config = toml.load('config.toml')
app = Flask(config.get("app_name"))
db = Database(app)
api = API(app)

api.add_resource(HelloWorld, '/')

def get_app():
    return app