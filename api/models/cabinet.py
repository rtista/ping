from . import Base

from sqlalchemy import Column, Integer, String


class Cabinet(Base):

    __tablename__ = 'cabinet'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255), nullable=False)
    height = Column('height', Integer, nullable=False)
