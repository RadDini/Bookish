from flask import request
import werkzeug

from bookish.services.user_services import *


def user_routes(app):
    @app.route('/register', methods=['POST'])
    def handle_register():
        if request.is_json:
            data = request.get_json()

            password = encrypt_password(data['password'])

            add_user(data['name'], password, data['email'])

            return {"message": "New user has been created successfully."}
        else:
            raise werkzeug.exceptions.UnprocessableEntity("Please enter a valid JSON.")

    @app.route('/get_users', methods=['GET'])
    def handle_get_users():

        return {"users": get_users()}

    @app.route('/login', methods=['POST'])
    def handle_login():
        if request.is_json:
            data = request.get_json()

            user = login(data)

            return update_token(user, data)
        else:
            raise werkzeug.exceptions.UnprocessableEntity("Please enter a valid JSON.")

    @app.route('/logout', methods=['POST'])
    def handle_logout():

        user_token = request.headers.get('Authorization')

        return remove_token(user_token)

    @app.route('/delete_user', methods=['DELETE'])
    def handle_delete_user():
        if request.is_json:
            user_token = request.headers.get('Authorization')

            if not user_token:
                raise werkzeug.exceptions.Unauthorized("User not logged in")

            user = find_user(user_token)

            if not user.is_admin:
                raise werkzeug.exceptions.PermissionDenied("User is not admin")
            return delete_user(request)
        else:
            raise werkzeug.exceptions.UnprocessableEntity("Please enter a valid JSON.")
