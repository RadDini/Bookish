import bcrypt
import jwt

from bookish.models import db
from bookish.models.book import Books
from bookish.models.borrowed_book import Borrowed_books
from bookish.models.user import Users
from bookish.services.error_handlers import *


def encrypt_password(password):
    salt = bcrypt.gensalt()
    bytes = password.encode('utf-8')

    hashed = bcrypt.hashpw(bytes, salt)
    hashed_password = hashed.decode("utf-8", "ignore")

    return hashed_password


def add_user(name, password, email):
    new_user = Users(name=name, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()


def update_token(user, data):
    token = jwt.encode(payload=data, key='secret', algorithm='HS256')
    token_str = str(token)[0:80]

    user.token = token_str
    db.session.commit()

    return token_str

def get_users():
    users = Users.query.all()
    return [{
        'id': user.id,
        'name': user.name,
        'password': user.password,
        'email': user.email
    } for user in users]

def login(data):
    user = Users.query.filter_by(email=data['email']).first()

    if not user:
        raise UserNotFound()

    if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        raise InvalidCredentials()

    return user

def remove_token(user_token):
    user = Users.query.filter_by(token=user_token).first()

    if not user:
        raise UserNotLoggedIn()

    user.token = None
    db.session.commit()

def find_user(user_token):
    user = Users.query.filter_by(token=user_token).first()

    if not user:
        raise UserNotFound()

    return user

def delete_user(request):
    data = request.get_json()

    user = Users.query.get(data['id'])

    if not user:
        raise UserNotFound()

    borrowed_books = Borrowed_books.query.filter_by(user_id=data['id'])

    for borrowed_book in borrowed_books:

        book = Books.query.filter_by(ISBN=borrowed_book.book_ISBN).first()

        book.copies_available += 1
        db.session.delete(borrowed_book)
        db.session.commit()

    db.session.delete(user)
    db.session.commit()

    return {"message": "User deleted successfully."}
