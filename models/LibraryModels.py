from initialize import db
from sqlalchemy_serializer import SerializerMixin


class AuthorModel(db.Model, SerializerMixin):
    __tablename__ = "author"
    datetime_format = '%d/%m/%Y'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=True)
    death_date = db.Column(db.DateTime, nullable=True)
    author_image = db.Column(db.String, unique=False,
                             nullable=False, default="default_user_image.jpg")

    def __repr__(self):
        return '<Author %r>' % self.name


class PublisherModel(db.Model, SerializerMixin):
    __tablename__ = "publisher"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Publisher %r>' % self.name


class CategoryModel(db.Model, SerializerMixin):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name


class BookModel(db.Model, SerializerMixin):
    __tablename__ = "book"
    datetime_format = '%d/%m/%Y'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    published_date = db.Column(db.DateTime, nullable=True)
    book_cover = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, default=1, nullable=False)
    author = db.relationship("AuthorModel")
    category = db.relationship("CategoryModel")
    publisher = db.relationship("PublisherModel")
    author_id = db.Column(db.Integer, db.ForeignKey(
        'author.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey(
        'publisher.id'), nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.name
