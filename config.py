from os import environ, path

basedir = path.abspath(path.dirname(__file__))

class Config(object):
    """Set Flask configurations vars from .env file."""

    # General
    TESTING = environ.get('TESTING')
    FLASK_DEBUG = environ.get('FLASK_DEBUG')
    SECRET_KEY = environ.get('SECRET_KEY') or 'secret_key'

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URL') or \
                              'sqlite:///' + path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis
    REDIS_URL = environ.get('REDIS_URL') or 'redis://'
