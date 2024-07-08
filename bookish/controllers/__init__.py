from bookish.controllers.bookish import bookish_routes
from bookish.controllers.BookController import book_routes
from bookish.controllers.UserController import user_routes


def register_controllers(app):
    bookish_routes(app)
    book_routes(app)
    user_routes(app)
