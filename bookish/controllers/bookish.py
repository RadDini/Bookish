from flask import request
from bookish.models.example import Example
from bookish.models.user import Users
from bookish.models.book import Books
from bookish.models.borrowed_book import Borrowed_books
from bookish.models import db, user

import bcrypt


def bookish_routes(app):
    @app.route('/healthcheck')
    def health_check():
        return {"status": "OK vreau acasa"}

    @app.route('/example', methods=['POST', 'GET'])
    def handle_example():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                new_example = Example(data1=data['data1'], data2=data['data2'])
                db.session.add(new_example)
                db.session.commit()
                return {"message": "New example has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}

        elif request.method == 'GET':
            examples = Example.query.all()
            results = [
                {
                    'id': example.id,
                    'data1': example.data1,
                    'data2': example.data2
                } for example in examples]
            return {"examples": results}

    @app.route('/register', methods=['POST'])
    def handle_register():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                salt = bcrypt.gensalt()
                bytes = data['password'].encode('utf-8')

                hashed = bcrypt.hashpw(bytes, salt)
                password = hashed.decode("utf-8", "ignore")

                new_user = Users(name=data['name'], password=password, email=data['email'])
                db.session.add(new_user)
                db.session.commit()
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

    @app.route('/books', methods=['POST', 'GET'])
    def handle_books():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                new_book = Books(ISBN=data['ISBN'], title=data['title'], author=data['author'],
                                 copies_available=data['copies_available'], copies_total=data['copies_total'])
                db.session.add(new_book)
                db.session.commit()
                return {"message": "New book has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}

        elif request.method == 'GET':
            books = Books.query.all()
            results = [{
                    'ISBN': book.ISBN,
                    'title': book.title,
                    'author': book.author,
                    'copies_available': book.copies_available,
                    'copies_total': book.copies_total
                } for book in books]
            return {"books": results}
