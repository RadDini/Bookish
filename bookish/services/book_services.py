import werkzeug

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


def get_books(order=None, limit=None):
    books = Books.query.all()
    if len(books) == 0:
        raise BookNotFound()

    if order is not None:
        if order.lower() == 'asc':
            books.sort(key=lambda b: b.title)
        elif order.lower() == 'desc':
            books.sort(key=lambda b: b.title, reverse=True)
        else:
            raise NotImplemented

    if limit is not None:
        try:
            limit = int(limit)
            books = books[0:limit]
        except ValueError:
            raise werkzeug.exceptions.BadRequest

    results = [{
        'ISBN': book.ISBN,
        'title': book.title,
        'author': book.author,
        'copies_available': book.copies_available,
        'copies_total': book.copies_total,
    } for book in books]

    return {"books": results}


def find_book(ISBN):
    return Books.query.filter_by(ISBN=ISBN).first().serialize()


def get_borrowed_books(request):
    user_token = request.headers.get('Authorization')

    user = Users.query.filter_by(token=user_token).first()

    if not user:
        raise UserNotFound()

    borrowed_books = Borrowed_books.query.filter_by(user_id=user.id)

    if not borrowed_books:
        raise BookNotFound()

    books = [(Books.query.get(book.book_ISBN), book.due_date) for book in borrowed_books]
    results = [{
        'ISBN': book[0].ISBN,
        'title': book[0].title,
        'author': book[0].author,
        'copies_available': book[0].copies_available,
        'copies_total': book[0].copies_total,
        'due_date': book[1]
    } for book in books]
    return {"books": results}


def borrow_book(request):
    data = request.get_json()

    user_token = request.headers.get('Authorization')

    user = Users.query.filter_by(token=user_token).first()

    if not user:
        raise UserNotFound()

    verify_fields(data, ['book_ISBN'])

    borrowed_book = Borrowed_books.query.filter_by(user_id=user.id).filter_by(book_ISBN=data['book_ISBN']).first()
    if borrowed_book:
        raise BookAlreadyBorrowed()

    book = Books.query.get(data['book_ISBN'])

    if book.copies_available <= 0:
        raise NoAvailableCopies()

    book.copies_available -= 1
    db.session.commit()

    new_borrowed_book = Borrowed_books(book_ISBN=data['book_ISBN'], user_id=user.id, due_date=data['due_date'])
    db.session.add(new_borrowed_book)
    db.session.commit()

    return {"message": "User has borrowed book successfully."}


def turn_in_book(request):
    data = request.get_json()

    user_token = request.headers.get('Authorization')

    user = Users.query.filter_by(token=user_token).first()

    if not user:
        raise UserNotFound()

    verify_fields(data, ['book_ISBN'])

    borrowed_book = Borrowed_books.query.filter_by(user_id=user.id).filter_by(book_ISBN=data['book_ISBN']).first()
    if not borrowed_book:
        raise BookNotBorrowed()

    book = Books.query.get(data['book_ISBN'])

    book.copies_available += 1

    db.session.delete(borrowed_book)
    db.session.commit()

    return {"message": "User has borrowed book successfully."}


def delete_book(request):
    data = request.get_json()

    verify_fields(data, ['ISBN'])

    book = Books.query.get(data['ISBN'])

    if not book:
        raise BookNotFound()

    borrowed_books = Borrowed_books.query.filter_by(book_ISBN=data['ISBN'])

    for borrowed_book in borrowed_books:
        db.session.delete(borrowed_book)
        db.session.commit()

    db.session.delete(book)
    db.session.commit()

    return {"message": "Book deleted successfully."}
