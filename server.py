from flask import Flask
from flask_restful import Resource, Api
import toml

config = toml.load('config.toml')
print(config)

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)