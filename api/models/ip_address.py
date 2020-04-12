from . import Base

from sqlalchemy import Column, String, ForeignKey, Integer


class IpAddress(Base):

    __tablename__ = 'ipaddress'

    address = Column('address', String(40), primary_key=True)
    range_id = Column('range_id', Integer, ForeignKey('range.id'), nullable=False)
    host_id = Column('host_id', Integer, ForeignKey('host.id'), nullable=False)
