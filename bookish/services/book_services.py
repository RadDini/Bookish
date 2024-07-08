from bookish.models import db
from bookish.models.book import Books
from bookish.models.borrowed_book import Borrowed_books
from bookish.models.user import Users


def add_book(data):
    new_book = Books(ISBN=data['ISBN'], title=data['title'], author=data['author'],
                     copies_available=data['copies_available'], copies_total=data['copies_total'])
    db.session.add(new_book)
    db.session.commit()

def get_books():
    books = Books.query.all()
    if len(books) == 0:
        return {"error": "No books found"}
    results = [{
        'ISBN': book.ISBN,
        'title': book.title,
        'author': book.author,
        'copies_available': book.copies_available,
        'copies_total': book.copies_total,
    } for book in books]
    return {"books": results}

def get_borrowed_books(request):
    user_token = request.headers.get('Authorization')

    if not user_token:
        return {"error": "User is not logged in"}

    user = Users.query.filter_by(token=user_token).first()

    if not user:
        return {"error": "User does not exist"}

    borrowed_books = Borrowed_books.query.filter_by(user_id=user.id)

    if not borrowed_books:
        return {"message": "No borrowed books found"}

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

    if not user_token:
        return {"error": "User is not logged in"}

    user = Users.query.filter_by(token=user_token).first()

    if not user:
        return {"error": "User does not exist"}

    borrowed_book = Borrowed_books.query.filter_by(user_id=user.id).filter_by(book_ISBN=data['book_ISBN']).first()
    if borrowed_book:
        return {"error": "Book already borrowed"}

    book = Books.query.get(data['book_ISBN'])

    if book.copies_available <= 0:
        return {"error": "No available copies"}

    book.copies_available -= 1
    db.session.commit()

    new_borrowed_book = Borrowed_books(book_ISBN=data['book_ISBN'], user_id=user.id, due_date=data['due_date'])
    db.session.add(new_borrowed_book)
    db.session.commit()

    return {"message": "User has borrowed book successfully."}

