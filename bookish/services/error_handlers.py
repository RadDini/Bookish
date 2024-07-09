import werkzeug


class WrongFormat(werkzeug.exceptions.HTTPException):
    code = 422
    description = 'The request payload is not in JSON format.'


class UserNotFound(werkzeug.exceptions.HTTPException):
    code = 404
    description = 'User does not exist.'


class InvalidCredentials(werkzeug.exceptions.HTTPException):
    code = 401
    description = 'Invalid credentials.'


class UserNotLoggedIn(werkzeug.exceptions.HTTPException):
    code = 401
    description = 'User is not logged in.'


class BookNotFound(werkzeug.exceptions.HTTPException):
    code = 404
    description = 'No books found.'


class BookAlreadyBorrowed(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Book is already borrowed.'


class NoAvailableCopies(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'No available copies found.'


class BookNotBorrowed(werkzeug.exceptions.HTTPException):
    code = 404
    description = 'Book is not borrowed.'


class PermissionDenied(werkzeug.exceptions.HTTPException):
    code = 404
    description = 'User is not admin.'


class MissingField(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Field is missing.'

    def __init__(self, missing_fields):
        self.missing_fields = missing_fields


def missing_field_handler(e):
    ret = ""

    for field in e.missing_fields:
        ret += "Missing field: " + field + "\n"

    return werkzeug.exceptions.UnprocessableEntity(description=ret)


def verify_fields(data, fields):
    missing_fields = []
    for field in fields:
        if field not in data:
            missing_fields.append(field)

    if len(missing_fields) > 0:
        raise MissingField(missing_fields)
