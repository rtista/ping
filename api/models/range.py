from . import Base

from sqlalchemy import Column, Integer, String


class Range(Base):

    __tablename__ = 'range'

    range_id = Column('id', Integer, primary_key=True)
    start_ip = Column('start_ip', String(40), nullable=False)
    netmask = Column('netmask', String(50), nullable=False)
