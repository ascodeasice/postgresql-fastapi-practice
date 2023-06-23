from datetime import datetime

from sqlalchemy import Column, Date, Integer, String, UnicodeText
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(UnicodeText, nullable=False)
    birthday = Column(Date)
    created_time = Column(Date, default=datetime.now())
    last_login = Column(Date, nullable=True)
