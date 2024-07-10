import werkzeug

from flask import jsonify

from bookish.models import db
from bookish.models.book import Books
from bookish.models.borrowed_book import Borrowed_books
from bookish.models.user import Users
from bookish.services.error_handlers import *


def add_book(data):
    verify_fields(data, ['ISBN', 'title', 'author', 'copies_available', 'copies_total'])

    new_book = Books(ISBN=data['ISBN'], title=data['title'], author=data['author'],
                     copies_available=data['copies_available'], copies_total=data['copies_total'])
    db.session.add(new_book)
    db.session.commit()

    return jsonify("Book added successfully")


def get_books(order=None, limit=None):
    books = Books.query.all()
    if len(books) == 0:
        raise werkzeug.exceptions.NotFound(description='Books not found')

    if order is not None:
        if order.lower() == 'asc':
            books.sort(key=lambda b: b.title)
        elif order.lower() == 'desc':
            books.sort(key=lambda b: b.title, reverse=True)
        else:
            raise werkzeug.exceptions.BadRequest(description='Order must be either ASC or DESC')

    if limit is not None:
        try:
            limit = int(limit)
            books = books[0:limit]
        except ValueError:
            raise werkzeug.exceptions.BadRequest

    return jsonify(books)


def find_book(ISBN):
    return jsonify(Books.query.filter_by(ISBN=ISBN).first().serialize())


def get_borrowed_books(request):
    user_token = request.headers.get('Authorization')

    user = Users.query.filter_by(token=user_token).first()

    if not user:
        raise werkzeug.exceptions.NotFound('User does not exist')

    borrowed_books = Borrowed_books.query.filter_by(user_id=user.id)

    if not borrowed_books:
        raise werkzeug.exceptions.NotFound(description='No books found')

    books = [(Books.query.get(book.book_ISBN).serialize() | {"due date": book.due_date}) for book in borrowed_books]

    return jsonify(books)


def borrow_book(request):
    data = request.get_json()

    user_token = request.headers.get('Authorization')

    user = Users.query.filter_by(token=user_token).first()

    if not user:
        raise werkzeug.exceptions.NotFound(description='User does not exist.')

    verify_fields(data, ['book_ISBN'])

    borrowed_book = Borrowed_books.query.filter_by(user_id=user.id).filter_by(book_ISBN=data['book_ISBN']).first()
    if borrowed_book:
        raise werkzeug.exceptions.BadRequest(description='Book already borrowed.')

    book = Books.query.get(data['book_ISBN'])

    if book.copies_available <= 0:
        raise werkzeug.exceptions.BadRequest(description='No available copies')

    book.copies_available -= 1

    new_borrowed_book = Borrowed_books(book_ISBN=data['book_ISBN'], user_id=user.id, due_date=data['due_date'])
    db.session.add(new_borrowed_book)
    db.session.commit()

    return jsonify("User has borrowed book successfully.")


def turn_in_book(request):
    data = request.get_json()

    user_token = request.headers.get('Authorization')

    user = Users.query.filter_by(token=user_token).first()

    if not user:
        raise werkzeug.exceptions.NotFound(description='User does not exist.')

    verify_fields(data, ['book_ISBN'])

    borrowed_book = Borrowed_books.query.filter_by(user_id=user.id).filter_by(book_ISBN=data['book_ISBN']).first()
    if not borrowed_book:
        raise werkzeug.exceptions.BadRequest(description='Book is not borrowed.')

    book = Books.query.get(data['book_ISBN'])

    book.copies_available += 1

    db.session.delete(borrowed_book)
    db.session.commit()

    return jsonify("User has turned in book successfully.")


def delete_book(request):
    data = request.get_json()

    verify_fields(data, ['ISBN'])

    book = Books.query.get(data['ISBN'])

    if not book:
        raise werkzeug.exceptions.NotFound(description='Book not found')

    borrowed_books = Borrowed_books.query.filter_by(book_ISBN=data['ISBN'])

    for borrowed_book in borrowed_books:
        db.session.delete(borrowed_book)

    db.session.delete(book)
    db.session.commit()

    return jsonify("Book deleted successfully.")
