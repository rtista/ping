from . import Base

from time import time

from sqlalchemy import Column, Integer, String


class User(Base):

    __tablename__ = 'user'

    id = Column('id', Integer, primary_key=True)
    account_id = Column('account_id', Integer, nullable=False)
    username = Column('username', String(16), unique=True, nullable=False)
    password = Column('password', String(100), nullable=False)
    name = Column('name', String(50), nullable=True)
    created = Column('created', Integer, default=int(time()))
