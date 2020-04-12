from . import Base

from sqlalchemy import Column, Integer, String, Enum


class Host(Base):
    __tablename__ = 'host'

    id = Column('id', Integer, primary_key=True)
    type = Column('type', Enum('bm,vm,ct'), nullable=False)
    hostname = Column('hostname', String(255), nullable=True)
    cpucores = Column('cpucores', Integer, nullable=True)
    ram = Column('ram', Integer, nullable=True)
    disk_size = Column('disk_size', Integer, nullable=True)
