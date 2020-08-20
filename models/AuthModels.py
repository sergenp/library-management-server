import datetime
from initialize import app, db, bcrypt, config
from sqlalchemy_serializer import SerializerMixin
import jwt

class UserModel(db.Model, SerializerMixin):
    __tablename__ ="users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    about = db.Column(db.String)
    birth_date = db.Column(db.DateTime, nullable=True)
    user_image = db.Column(db.String, default="default_user_image.jpg")
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)
        self.password = bcrypt.generate_password_hash(
            self.password, config.get('bcrypt').get('bcrypt_log_rounds')
        ).decode()
        self.registered_on = datetime.datetime.now()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
        
    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=4),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            ).decode('utf-8')
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return '<User %r>' % self.id