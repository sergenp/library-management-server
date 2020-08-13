import os
import werkzeug
import toml
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from flask import request
from flask_restful import Resource, reqparse
from models.Models import CategoryModel, AuthorModel, BookModel, db


ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

config = toml.load("./config.toml")
UPLOAD_FOLDER = "/".join(config.get("file").get("path"))

def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


class Author(Resource):
    def get(self, author_id):
        author = AuthorModel.query.get_or_404(author_id, description="Author is not found")
        return {'data' : {'author' : author.to_dict()}}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help="name field is required")
        data = parser.parse_args()
        author = AuthorModel(name=data['name'])
        db.session.add(author)
        db.session.commit()
        return {'data' : { "author" : author.to_dict()}}, 201

class Category(Resource):
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id, description="Category is not found")
        return {'data' : {'category' : category.to_dict()}}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help="name field is required")
        data = parser.parse_args()
        category = CategoryModel(name=data['name'])
        db.session.add(category)
        db.session.commit()
        return {'data' : { "category" : category.to_dict()}}, 201

class Book(Resource):
    def get(self, book_id):
        book = BookModel.query.get_or_404(book_id, description="Book is not found")
        return {'data' : {'book' : book.to_dict()}}, 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help="name field is required", required=True)
        parser.add_argument('author_id', type=int, help="author_id field is required", required=True)
        parser.add_argument('category_id', type=int, help="category_id field is required", required=True)
        parser.add_argument('published_date', type=str, help="published_date field is required", required=True)
        parser.add_argument('book_cover', type=werkzeug.datastructures.FileStorage, location='files', help=f"You must provide a book cover image, allowed extensions are {','.join(ALLOWED_IMAGE_EXTENSIONS)}", required=True)
        data = parser.parse_args()
        
        if allowed_image(data['book_cover'].filename):
            filename = f"{uuid.uuid1()}.{data['book_cover'].filename.split('.')[1]}" 
        else:
            return {'message' : f"Given file cant be processed,allowed extensions are {','.join(ALLOWED_IMAGE_EXTENSIONS)}"}, 400

        author = AuthorModel.query.filter_by(id=data['author_id']).first_or_404(description=f"Author with id {data['author_id']} is not found")
        category = CategoryModel.query.filter_by(id=data['category_id']).first_or_404(description=f"Category with id {data['category_id']} is not found")
        try:
            published_date = datetime.strptime(data['published_date'], '%d/%m/%Y')
        except ValueError:
            return {'message' : 'Given date is not in the format of %d/%m/%Y'}, 400

        new_book = BookModel(name=data['name'], published_date=published_date, author=author, category=category, book_cover=filename)
        try:
            db.session.add(new_book)
            db.session.commit()
            data['book_cover'].save(os.path.join(UPLOAD_FOLDER, filename))
            return {'data' : {'book': new_book.to_dict()}}, 201
        except IntegrityError as e:
            return {'message' : 'Book already is in the database'}, 400


