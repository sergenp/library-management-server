import os
from flask import send_from_directory, Response, redirect
from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import HTTPException
from initialize import app, api, admin, db, basic_auth, jwt
# importing Resources is important. Whatever Database model the resource has will get created using flask db migrate/upgrade. Otherwise models wont be added/updated in the database
from api.LibraryResources import Book, Author, Category, Publisher, BookModel, AuthorModel, CategoryModel, PublisherModel
from api.AuthResources import User, Register, Login, LogoutAccess, LogoutRefresh, TokenRefresh, RevokedTokenModel, UserModel

# API ENDPOINTS
api.add_resource(Book, '/books/<int:book_id>', '/books')
api.add_resource(Author, '/authors/<int:author_id>', '/authors')
api.add_resource(Category, '/categories/<int:category_id>', '/categories')
api.add_resource(Publisher, '/publishers/<int:publisher_id>', '/publishers')
api.add_resource(User, '/users')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(LogoutAccess, '/logoutaccess')
api.add_resource(LogoutRefresh, '/logoutrefresh')
api.add_resource(TokenRefresh, '/refreshtoken')

class AdminPageModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise HTTPException("Login Required", Response(
             "Login Required", 401,
             {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))
        else:
            return True
            
    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

# ADMIN PAGES
admin.add_view(AdminPageModelView(UserModel, db.session))
admin.add_view(AdminPageModelView(BookModel, db.session))
admin.add_view(AdminPageModelView(AuthorModel, db.session))
admin.add_view(AdminPageModelView(CategoryModel, db.session))
admin.add_view(AdminPageModelView(PublisherModel, db.session))
admin.add_view(AdminPageModelView(RevokedTokenModel, db.session))

@app.route('/files/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

if __name__ == '__main__':
    app.run()
