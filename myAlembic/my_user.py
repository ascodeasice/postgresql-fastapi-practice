from datetime import datetime

from sqlalchemy import Column, Date, DateTime, UnicodeText
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    username = Column(UnicodeText, primary_key=True)
    password = Column(UnicodeText, nullable=False)
    birthday = Column(Date)
    created_time = Column(DateTime, default=datetime.utcnow)
    last_login = Column(Date, nullable=True)
