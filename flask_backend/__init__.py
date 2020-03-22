from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from db.schemas import AlarmSchema

migrate = Migrate()
bootstrap = Bootstrap()
db = SQLAlchemy()
alarm_schema = AlarmSchema()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    bootstrap.init_app(app)
    db.init_app(app)

    with app.app_context():
        from . import routes

    return app
