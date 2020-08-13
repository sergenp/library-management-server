import os
from db.database import app, db, config
from flask import send_from_directory
from flask_restful import Api
from api.Resources import Book, Author, Category
# need to import models to initialize database using create_all method
from models.Models import CategoryModel, AuthorModel, BookModel 

db.create_all()
app.config['UPLOAD_FOLDER'] = os.path.join(*config.get("file").get("path"))
api = Api(app)
api.add_resource(Book, '/books/<int:book_id>', '/books')
api.add_resource(Author, '/authors/<int:author_id>', '/authors')
api.add_resource(Category, '/categories/<int:category_id>', '/categories')

@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(debug=True)