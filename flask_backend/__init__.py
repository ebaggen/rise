from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_rq2 import RQ
ma = Marshmallow()
rq = RQ()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    from .models import db

    db.init_app(app)
    ma.init_app(app)
    rq.init_app(app)

    with app.app_context():
        from . import routes, scheduler

        scheduler.schedule_alarm()

    return app



