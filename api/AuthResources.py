from flask_restful import Resource, reqparse
from models.AuthModels import UserModel


class User(Resource):
    def get(self, user_id):
        user = UserModel.query.get_or_404(
            user_id, description="User is not found")
        return {'data': {'user': user.to_dict()}}, 200
