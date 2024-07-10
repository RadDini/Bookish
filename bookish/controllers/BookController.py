import json

from flask import request
import werkzeug

from bookish.services.book_services import *
from bookish.services.user_services import find_user


def book_routes(app):
    @app.route('/books', methods=['POST', 'GET'])
    def handle_books():
        user_token = request.headers.get('Authorization')

        if not user_token:
            raise werkzeug.exceptions.Unauthorized("User not logged in")

        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()

                return add_book(data)
            else:
                raise werkzeug.exceptions.UnprocessableEntity("Please enter a valid JSON.")
        elif request.method == 'GET':

            return get_books(order=request.args.get('order'), limit=request.args.get('limit'))

    @app.route('/book/<string:ISBN>', methods=['GET'])
    def handle_book(ISBN):
        return find_book(ISBN)

    @app.route('/borrow_book', methods=['POST'])
    def handle_borrow_book():
        if request.method == 'POST':
            if request.is_json:
                user_token = request.headers.get('Authorization')

                if not user_token:
                    raise werkzeug.exceptions.Unauthorized("User not logged in")

                return borrow_book(request)
            else:
                raise werkzeug.exceptions.UnprocessableEntity("Please enter a valid JSON.")

    @app.route('/get_borrowed_books', methods=['GET'])
    def handle_borrowed_books():
        user_token = request.headers.get('Authorization')

        if not user_token:
            raise werkzeug.exceptions.Unauthorized("User not logged in")

        return get_borrowed_books(request)

    @app.route('/turn_in_book', methods=['POST'])
    def handle_turn_in_book():
        if request.is_json:
            user_token = request.headers.get('Authorization')

            if not user_token:
                raise werkzeug.exceptions.Unauthorized("User not logged in")

            return turn_in_book(request)
        else:
            raise werkzeug.exceptions.UnprocessableEntity("Please enter a valid JSON.")

    @app.route('/delete_book', methods=['DELETE'])
    def handle_delete_book():
        if request.is_json:
            user_token = request.headers.get('Authorization')

            if not user_token:
                raise werkzeug.exceptions.Unauthorized("User not logged in")

            user = find_user(user_token)

            if not user.is_admin:
                raise werkzeug.exceptions.PermissionDenied("User is not admin")

            return delete_book(request)
        else:
            raise werkzeug.exceptions.UnprocessableEntity("Please enter a valid JSON.")
