from flask_restful import Api, Resource

class API:
    def __init__(self, app):
        self.api = Api(app)

    def add_resource(self, resource: Resource, path: str):
        self.api.add_resource(resource, path)
