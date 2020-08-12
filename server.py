import os
from db.database import app, db
from flask_restful import Api
from api.Resources import HelloWorld, Book, Author
# need to import models to initialize database using create_all method
from models.Models import AuthorModel, BookModel

db.create_all()
api = Api(app)
api.add_resource(HelloWorld, '/')
api.add_resource(Book, '/books/<int:book_id>', '/books')
api.add_resource(Author, '/authors/<int:author_id>', '/authors')

if __name__ == '__main__':
    app.run(debug=True)