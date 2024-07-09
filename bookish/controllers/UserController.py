import bcrypt
from flask import request

from bookish.services.user_services import *
from bookish.services.error_handlers import *


def user_routes(app):
    @app.route('/register', methods=['POST'])
    def handle_register():
        if request.is_json:
            data = request.get_json()

            password = encrypt_password(data['password'])

            add_user(data['name'], password, data['email'])

            return {"message": "New user has been created successfully."}
        else:
            raise WrongFormat()

    @app.route('/get_users', methods=['GET'])
    def handle_get_users():

        return {"users": get_users()}

    @app.route('/login', methods=['POST'])
    def handle_login():
        if request.is_json:
            data = request.get_json()

            user = login(data)

            return {"message": "User logged in successfully.", "token": update_token(user, data)}
        else:
            raise WrongFormat()

    @app.route('/logout', methods=['POST'])
    def handle_logout():

        user_token = request.headers.get('Authorization')

        remove_token(user_token)

        return {"message": "User logged out successfully."}

    @app.route('/delete_user', methods=['DELETE'])
    def handle_delete_user():
        if request.is_json:
            user_token = request.headers.get('Authorization')

            if not user_token:
                raise UserNotLoggedIn()

            user = find_user(user_token)

            if not user.is_admin:
                raise PermissionDenied()

            return delete_user(request), 200
        else:
            raise WrongFormat()
