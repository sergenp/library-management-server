from db.database import db
from sqlalchemy_serializer import SerializerMixin

class AuthorModel(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Author %r>' % self.name

class PublisherModel(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Publisher %r>' % self.name

class CategoryModel(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    
    def __repr__(self):
        return '<Category %r>' % self.name


class BookModel(db.Model, SerializerMixin):
    datetime_format = '%d/%m/%Y'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    published_date = db.Column(db.DateTime, nullable=True)
    book_cover = db.Column(db.String, unique=True, nullable=False)
    author = db.relationship("AuthorModel")
    category = db.relationship("CategoryModel")
    publisher = db.relationship("PublisherModel")
    author_id = db.Column(db.Integer, db.ForeignKey('author_model.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category_model.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher_model.id'), nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.name
