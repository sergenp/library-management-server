import os
from db.database import app, db
from flask_restful import Api
from api.Resources import Book, Author, Category
# need to import models to initialize database using create_all method
from models.Models import CategoryModel, AuthorModel, BookModel 

db.create_all()
api = Api(app)
api.add_resource(Book, '/books/<int:book_id>', '/books')
api.add_resource(Author, '/authors/<int:author_id>', '/authors')
api.add_resource(Category, '/categories/<int:category_id>', '/categories')

if __name__ == '__main__':
    app.run(debug=True)