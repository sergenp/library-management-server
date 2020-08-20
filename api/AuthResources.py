from flask_restful import Resource, reqparse
from models.AuthModels import UserModel, db, config, bcrypt
from .resource_util import ALLOWED_IMAGE_EXTENSIONS, UPLOAD_FOLDER, check_image, date_type
from sqlalchemy import exc


class User(Resource):
    def get(self, user_id):
        user = UserModel.query.get_or_404(
            user_id, description="User is not found")
        return {'data': {'user': user.to_dict()}}, 200


class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'username', type=str, help="Username field is required", required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        data = parser.parse_args()
        try:
            user = UserModel(
                username=data['username'], email=data['email'], password=data['password'])
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            return {'message': 'Given username or email already exists'}, 400
        return {'data': {"user": user.to_dict(only=("id",)), "token": UserModel.encode_auth_token(user.id)}}, 201

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, help="Username field is required", required=True)
        parser.add_argument("password", type=str, help="Password field is required", required=True)
        data = parser.parse_args()
        user = UserModel.query.filter_by(username=data['username']).first()
        if user:
            password = user.check_password(data["password"])
            if password:
                return {'data': {"user": user.to_dict(only=("id",)), "token": UserModel.encode_auth_token(user.id)}}, 201
        return {'message' : 'Authentication failed, please check your username/password'}, 400
        