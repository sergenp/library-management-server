import datetime
from initialize import app, db, bcrypt, config
from sqlalchemy_serializer import SerializerMixin

class UserModel(db.Model, SerializerMixin):
    __tablename__ ="users"

    serialize_only = ('id','username','about','birth_date','user_image','email','registered_on')

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

    def __repr__(self):
        return '<User %r>' % self.id

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)