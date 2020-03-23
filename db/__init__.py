from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))
