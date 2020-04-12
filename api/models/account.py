from . import Base

from time import time

from sqlalchemy import Column, Integer, String


class Account(Base):

    __tablename__ = 'account'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255), nullable=False)
    created = Column('created', Integer, default=int(time()))
