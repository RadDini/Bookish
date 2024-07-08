from flask import request
from bookish.models.user import Users
from bookish.models.book import Books
from bookish.models.borrowed_book import Borrowed_books
from bookish.models import db, user
from bookish.services.book_services import *


def book_routes(app):
    @app.route('/books', methods=['POST', 'GET'])
    def handle_books():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()

                add_book(data)

                return {"message": "New book has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}

        elif request.method == 'GET':

            return get_books()
    @app.route('/book/<string:ISBN>', methods=['GET'])
    def handle_book(ISBN):
        book = Books.query.get_or_404(ISBN)
        return {"book": book.serialize()}

    @app.route('/borrow_book', methods=['POST'])
    def handle_borrow_book():
        if request.method == 'POST':
            if request.is_json:
                return borrow_book(request), 200
            else:
                return {"error": "The request payload is not in JSON format"}


    @app.route('/get_borrowed_books', methods=['GET'])
    def handle_borrowed_books():
        return get_borrowed_books(request)


