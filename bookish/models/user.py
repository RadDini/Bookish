from bookish.app import db


class Users(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'Users'

    # Here we outline what columns we want in our database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    token = db.Column(db.String(80))

    def __init__(self, name, password, email, token=None):
        self.name = name
        self.password = password
        self.email = email
        self.token = token

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'Name': self.name,
            'Password': self.password,
            'Email': self.email
        }
