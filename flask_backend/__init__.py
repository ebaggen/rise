from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from db import Session

bootstrap = Bootstrap()
session = Session


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    bootstrap.init_app(app)

    with app.app_context():
        from . import routes

    return app
