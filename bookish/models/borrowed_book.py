from bookish.app import db


class Borrowed_books(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'Borrowed_books'

    # Here we outline what columns we want in our database
    id = db.Column(db.Integer, primary_key=True)
    book_ISBN = db.Column(db.String(80), db.ForeignKey('Books.ISBN'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    due_date = db.Column(db.Date, nullable=False)

    def __init__(self, book_ISBN, user_id, due_date):
        self.book_ISBN = book_ISBN
        self.user_id = user_id
        self.due_date = due_date

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'book_ISBN': self.book_ISBN,
            'user_id': self.user_id,
            'due_date': self.due_date
        }
