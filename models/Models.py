from db.database import db
from sqlalchemy_serializer import SerializerMixin

class AuthorModel(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Author %r>' % self.name

class BookModel(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author_model.id'))
    author = db.relationship("AuthorModel")
    
    def __repr__(self):
        return '<Book %r>' % self.name
