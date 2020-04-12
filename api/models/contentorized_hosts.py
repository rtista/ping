from . import Base

from sqlalchemy import Column, Integer, ForeignKey


class ContentorizedHosts(Base):

    __tablename__ = 'contentorized_hosts'

    bm_id = Column('bm_id', Integer, ForeignKey('host.id'), nullable=False)
    virt_id = Column('virt_id', Integer, ForeignKey('host.id'), nullable=False)
