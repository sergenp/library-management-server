import os
from flask import send_from_directory
from flask_admin.contrib.sqla import ModelView
from initialize import app, api, admin, db
# importing Resources is important. Whatever Database model the resource has will get created using flask db migrate/upgrade. Otherwise models wont be added/updated in the database
from api.LibraryResources import Book, Author, Category, Publisher, BookModel, AuthorModel, CategoryModel, PublisherModel
from api.AuthResources import User, Register, Login, UserModel


# API ENDPOINTS
api.add_resource(Book, '/books/<int:book_id>', '/books')
api.add_resource(Author, '/authors/<int:author_id>', '/authors')
api.add_resource(Category, '/categories/<int:category_id>', '/categories')
api.add_resource(Publisher, '/publishers/<int:publisher_id>', '/publishers')
api.add_resource(User, '/users/<int:user_id>', '/users')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')

# ADMIN PAGES
admin.add_view(ModelView(UserModel, db.session))
admin.add_view(ModelView(BookModel, db.session))
admin.add_view(ModelView(AuthorModel, db.session))
admin.add_view(ModelView(CategoryModel, db.session))
admin.add_view(ModelView(PublisherModel, db.session))

@app.route('/files/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG_MODE'], port=app.config['PORT'])
