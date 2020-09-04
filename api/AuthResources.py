from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, jwt_required
from flask_restful import Resource, reqparse
from models.AuthModels import UserModel, RevokedTokenModel, db, config, bcrypt
from .resource_util import ALLOWED_IMAGE_EXTENSIONS, UPLOAD_FOLDER, check_image, date_type, email_type
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
        parser.add_argument('email', type=email_type, required=True, help="Given email is invalid")
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
        
        
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        return {'data': {"user": user.to_dict(only=("id",)), "access_token": access_token, "refresh_token" : refresh_token }}, 201

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
                access_token = create_access_token(identity=data['username'])
                refresh_token = create_refresh_token(identity=data['username'])
                return {'data': {"user": user.to_dict(only=("id",)), "access_token": access_token, "refresh_token" : refresh_token }}, 200
        return {'message' : 'Authentication failed, please check your username/password'}, 400
        
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}

class LogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        print(jti)
        try:
            db.session.add(RevokedTokenModel(jti = jti))
            db.session.commit()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class LogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            db.session.add(RevokedTokenModel(jti = jti))
            db.session.commit()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
