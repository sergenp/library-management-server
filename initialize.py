import os
from db.database import app, db
from api.Api import API
from api.Resources import HelloWorld



db.create_all()
api = API(app)
api.add_resource(HelloWorld, '/')
