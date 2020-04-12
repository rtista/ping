from . import Base

from sqlalchemy import Column, Integer, ForeignKey


class HostCabinet(Base):

    __tablename__ = 'host_cabinet'

    cabinet_id = Column('cabinet_id', Integer, ForeignKey('cabinet.id'), nullable=False)
    host_id = Column('host_id', Integer, ForeignKey('host.id'), nullable=False)
