import os
import werkzeug
import toml
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from flask import request
from flask_restful import Resource, reqparse
from models.Models import CategoryModel, AuthorModel, BookModel, PublisherModel, db


ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
CONFIG = toml.load("./config.toml")
UPLOAD_FOLDER = "/".join(CONFIG.get("file").get("path"))


def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def date_type(x): return datetime.strptime(x, '%d/%m/%Y')


class Author(Resource):
    def get(self, author_id):
        author = AuthorModel.query.get_or_404(
            author_id, description="Author is not found")
        return {'data': {'author': author.to_dict()}}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name', type=str, help="Name field is required", required=True)
        parser.add_argument(
            'about', type=str, help="You need to provide an about for the author", required=True)
        parser.add_argument('birth_date', type=date_type, default=None)
        parser.add_argument('death_date', type=date_type, default=None)
        data = parser.parse_args()
        author = AuthorModel(
            name=data['name'], about=data['about'], birth_date=data['birth_date'], death_date=data['death_date'])
        db.session.add(author)
        db.session.commit()
        return {'data': {"author": author.to_dict()}}, 201


class Category(Resource):
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(
            category_id, description="Category is not found")
        return {'data': {'category': category.to_dict()}}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help="name field is required")
        data = parser.parse_args()
        category = CategoryModel(name=data['name'])
        db.session.add(category)
        db.session.commit()
        return {'data': {"category": category.to_dict()}}, 201


class Publisher(Resource):
    def get(self, publisher_id):
        publisher = PublisherModel.query.get_or_404(
            publisher_id, description="Publisher is not found")
        return {'data': {'publisher': publisher.to_dict()}}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help="name field is required")
        data = parser.parse_args()
        publisher = PublisherModel(name=data['name'])
        db.session.add(publisher)
        db.session.commit()
        return {'data': {"publisher": publisher.to_dict()}}, 201


class Book(Resource):
    def get(self, book_id):
        book = BookModel.query.get_or_404(
            book_id, description="Book is not found")
        return {'data': {'book': book.to_dict()}}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name', type=str, help="Name field is required", required=True)
        parser.add_argument('author_id', type=int,
                            help="You must provide an author", required=True)
        parser.add_argument('category_id', type=int,
                            help="You must provide a category", required=True)
        
        parser.add_argument('published_date', type=date_type, default=None,
                            help="Date doesn't match day/month/year format")
        parser.add_argument('book_cover', type=werkzeug.datastructures.FileStorage, location='files',
                            help=f"You must provide a book cover image, allowed extensions are {','.join(ALLOWED_IMAGE_EXTENSIONS)}", required=True)
        parser.add_argument('description', type=str, required=True,
                            help='You must provide a book description')
        parser.add_argument('publisher_id', type=str, default=None)
        data = parser.parse_args()

        # these values might be None, we need to declare the variables to avaid ReferencedBeforeAssignment exception
        publisher = data['publisher_id']
        published_date = data['published_date']

        if allowed_image(data['book_cover'].filename):
            filename = f"{uuid.uuid1()}.{data['book_cover'].filename.split('.')[1]}"
        else:
            return {'message': f"Given file cant be processed,allowed extensions are {','.join(ALLOWED_IMAGE_EXTENSIONS)}"}, 400

        author = AuthorModel.query.filter_by(id=data['author_id']).first_or_404(
            description=f"Author with id {data['author_id']} is not found")
        category = CategoryModel.query.filter_by(id=data['category_id']).first_or_404(
            description=f"Category with id {data['category_id']} is not found")

        if publisher:
            publisher = PublisherModel.query.filter_by(id=publisher).first_or_404(
                description=f"Publisher with id {publisher} is not found")

        new_book = BookModel(name=data['name'], published_date=published_date, description=data['description'],
                             author=author, category=category, book_cover=filename, publisher=publisher)
        try:
            db.session.add(new_book)
            db.session.commit()
            data['book_cover'].save(os.path.join(UPLOAD_FOLDER, filename))
            return {'data': {'book': new_book.to_dict()}}, 201
        except IntegrityError as e:
            return {'message': 'Book already is in the database'}, 400
