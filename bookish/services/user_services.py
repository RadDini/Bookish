import bcrypt
import jwt

from bookish.models import db
from bookish.models.user import Users


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
