from datetime import datetime
from flask import request
from flask_restful import Resource
from models.Models import CategoryModel, AuthorModel, BookModel, db


class Author(Resource):
    def get(self, author_id):
        author = AuthorModel.query.get_or_404(author_id, description="Author is not found")
        return {'data' : {'author' : author.to_dict()}}, 200

    def post(self):
        data = request.get_json()
        author = AuthorModel(name=data['name'])
        db.session.add(author)
        db.session.commit()
        return {'data' : { "author" : author.to_dict()}}, 201

class Category(Resource):
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id, description="Category is not found")
        return {'data' : {'category' : category.to_dict()}}, 200

    def post(self):
        data = request.get_json()
        category = CategoryModel(name=data['name'])
        db.session.add(category)
        db.session.commit()
        return {'data' : { "category" : category.to_dict()}}, 201

class Book(Resource):
    def get(self, book_id):
        book = BookModel.query.get_or_404(book_id, description="Book is not found")
        return {'data' : {'book' : book.to_dict()}}, 200
    
    def post(self):
        data = request.get_json()
        author = AuthorModel.query.filter_by(id=data['author_id']).first_or_404(description=f"Author with id{data['author_id']} is not found")
        category = CategoryModel.query.filter_by(id=data['category_id']).first_or_404(description=f"Category with id {data['category_id']} is not found")
        try:
            published_date = datetime.strptime(data['published_date'], '%m/%d/%Y')
        except ValueError:
            return {'message' : 'Given date is not in the format of %m/%d/%Y'}, 400

        new_book = BookModel(name=data['name'], published_date=published_date, author=author, category=category)
        db.session.add(new_book)
        db.session.commit()
        return {'data' : {'book': new_book.to_dict()}}, 201


