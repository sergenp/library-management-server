from flask import request
from flask_restful import Resource
from models.Models import AuthorModel, BookModel, db


class Author(Resource):
    def get(self, author_id):
        author = AuthorModel.query.get_or_404(author_id, description="Author not found")
        return {'data' : {'author' : author.to_dict()}}, 200

    def post(self):
        data = request.get_json()
        author = AuthorModel(name=data['name'])
        db.session.add(author)
        db.session.commit()
        return {'data' : { "author" : author.to_dict()}}, 201

class Book(Resource):
    def get(self, book_id):
        book = BookModel.query.get_or_404(book_id, description="Book not found")
        return {'data' : {'book' : book.to_dict()}}, 200
    
    def post(self):
        data = request.get_json()
        author = AuthorModel.query.filter_by(id=data['author_id']).first()
        if author:
            new_book = BookModel(name=data['name'], author=author)
            db.session.add(new_book)
            db.session.commit()
            return {'data' : {'book': new_book.to_dict()}}, 201
        return {'error' : 'Failed to create a book, Author is not in the database'}, 400