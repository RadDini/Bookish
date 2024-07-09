import os
from flask import Flask
from bookish.models import db, migrate
from bookish.controllers import register_controllers
from bookish.services.error_handlers import *
from bookish.models.user import Users
from bookish.services.user_services import encrypt_password



def create_app():
    app = Flask(__name__)

    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    register_controllers(app)
    app.register_error_handler(WrongFormat, lambda x: x)
    app.register_error_handler(UserNotFound, lambda x: x)
    app.register_error_handler(InvalidCredentials, lambda x: x)
    app.register_error_handler(UserNotLoggedIn, lambda x: x)
    app.register_error_handler(BookNotFound, lambda x: x)
    app.register_error_handler(BookAlreadyBorrowed, lambda x: x)
    app.register_error_handler(NoAvailableCopies, lambda x: x)
    app.register_error_handler(BookNotBorrowed, lambda x: x)



    if __name__ == "__main__":
        app.run()

    return app
