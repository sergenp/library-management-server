from initialize import db, bcrypt
from sqlalchemy_serializer import SerializerMixin


class UserModel(db.Model, SerializerMixin):
    __tablename__ ="users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=True)
    birth_date = db.Column(db.DateTime, nullable=True)
    user_image = db.Column(db.String, unique=True, nullable=True, default="default_user_image.jpg")
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, config.get('bcrypt').get('bcrypt_log_rounds')
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def __repr__(self):
        return '<User %r>' % self.id