from flask import request
from bookish.services.book_services import *
from bookish.services.user_services import find_user
from bookish.services.error_handlers import *

def book_routes(app):

    @app.route('/books', methods=['POST', 'GET'])
    def handle_books():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()

                add_book(data)

                return {"message": "New book has been created successfully."}
            else:
                raise WrongFormat()


        elif request.method == 'GET':

            return get_books()

    @app.route('/book/<string:ISBN>', methods=['GET'])
    def handle_book(ISBN):
        return {"book": find_book(ISBN)}

    @app.route('/borrow_book', methods=['POST'])
    def handle_borrow_book():
        if request.method == 'POST':
            if request.is_json:
                user_token = request.headers.get('Authorization')

                if not user_token:
                    raise UserNotLoggedIn()

                return borrow_book(request), 200
            else:
                raise WrongFormat()

    @app.route('/get_borrowed_books', methods=['GET'])
    def handle_borrowed_books():
        user_token = request.headers.get('Authorization')

        if not user_token:
            raise UserNotLoggedIn()

        return get_borrowed_books(request)

    @app.route('/turn_in_book', methods=['POST'])
    def handle_turn_in_book():
        if request.is_json:
            user_token = request.headers.get('Authorization')

            if not user_token:
                raise UserNotLoggedIn()

            return turn_in_book(request), 200
        else:
            raise WrongFormat()

    @app.route('/delete_book', methods=['DELETE'])
    def handle_delete_book():
        if request.is_json:
            user_token = request.headers.get('Authorization')

            if not user_token:
                raise UserNotLoggedIn()

            user = find_user(user_token)

            if not user.is_admin:
                raise PermissionDenied()

            return delete_book(request), 200
        else:
            raise WrongFormat()

