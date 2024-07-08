from flask import request
from bookish.models.example import Example
from bookish.models.user import Users
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
                    'Name': user.name,
                    'Password': user.password,
                    'Email': user.email
                } for user in users]

            return {"users": results}


        else:
            return {"error": "Method not allowed"}


