from flask import request, session
from bookish.models.example import Example
from bookish.models.user import Users
from bookish.models.book import Books
from bookish.models.borrowed_book import Borrowed_books
from bookish.models import db, user
from bookish.services.user_services import *

import bcrypt






def user_routes(app):

    @app.route('/register', methods=['POST'])
    def handle_register():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()

                password = encrypt_password(data['password'])

                add_user(data['name'], password, data['email'])

                return {"message": "New user has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}

        else:
            return {"error": "Method not allowed"}

    @app.route('/get_users', methods=['GET'])
    def handle_get_users():
        if request.method == 'GET':
            users = Users.query.all()
            results = [{
                    'id': user.id,
                    'name': user.name,
                    'password': user.password,
                    'email': user.email
                } for user in users]

            return {"users": results}
        else:
            return {"error": "Method not allowed"}

    @app.route('/login', methods=['POST'])
    def handle_login():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                user = Users.query.filter_by(email=data['email']).first()

                if not user:
                    return {"error": "User does not exist"}

                if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    return {"error": "Invalid credentials"}, 401

                return {"message": "User logged in successfully.", "token": update_token(user, data)}
            else:
                return {"error": "The request payload is not in JSON format"}

        else:
            return {"error": "Method not allowed"}

    @app.route('/logout', methods=['POST'])
    def handle_logout():
        if request.method == 'POST':

            user_token = request.headers.get('Authorization')

            if not user_token:
                return {"error": "User is not logged in"}

            user = Users.query.filter_by(token=user_token).first()

            if not user:
                return {"error": "User does not exist"}
            user.token = None
            db.session.commit()

            return {"message": "User logged out successfully."}

        else:
            return {"error": "Method not allowed"}