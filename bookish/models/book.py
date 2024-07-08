from bookish.app import db


class Books(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'Books'

    # Here we outline what columns we want in our database
    ISBN = db.Column(db.String(80), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    copies_available = db.Column(db.Integer, nullable=False)
    copies_total = db.Column(db.Integer, nullable=False)

    def __init__(self, ISBN, title, author, copies_available, copies_total):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.copies_available = copies_available
        self.copies_total = copies_total

    def __repr__(self):
        return '<ISBN {}>'.format(self.ISBN)

    def serialize(self):
        return {
            'ISBN': self.ISBN,
            'title': self.title,
            'author': self.author,
            'copies_available': self.copies_available,
            'copies_total': self.copies_total
        }
