# Batteries
import time

# Third-party Imports
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# Create Base model class
Base = declarative_base()


def unixtime():
    """
    Helper class for integer unix timestamp generation.
    Returns:
        int: Unix timestamp as integer.
    """
    return int(time.time())


class Account(Base):

    __tablename__ = 'account'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255), nullable=False)
    created = Column('created', Integer, default=unixtime)


class Cabinet(Base):

    __tablename__ = 'cabinet'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255), nullable=False)
    height = Column('height', Integer, nullable=False)


class ContentorizedHosts(Base):

    __tablename__ = 'contentorized_hosts'

    bm_id = Column('bm_id', Integer, ForeignKey('host.id'), primary_key=True)
    virt_id = Column('virt_id', Integer, ForeignKey('host.id'), primary_key=True)


class HostCabinet(Base):

    __tablename__ = 'host_cabinet'

    cabinet_id = Column('cabinet_id', Integer, ForeignKey('cabinet.id'), primary_key=True)
    host_id = Column('host_id', Integer, ForeignKey('host.id'), primary_key=True)


class Host(Base):
    __tablename__ = 'host'

    id = Column('id', Integer, primary_key=True)
    type = Column('type', Enum('bm,vm,ct'), nullable=False)
    hostname = Column('hostname', String(255), nullable=True)
    cpucores = Column('cpucores', Integer, nullable=True)
    ram = Column('ram', Integer, nullable=True)
    disk_size = Column('disk_size', Integer, nullable=True)


class IpAddress(Base):

    __tablename__ = 'ipaddress'

    address = Column('address', String(40), primary_key=True)
    range_id = Column('range_id', Integer, ForeignKey('range.id'), nullable=False)
    host_id = Column('host_id', Integer, ForeignKey('host.id'), nullable=False)


class Range(Base):

    __tablename__ = 'range'

    range_id = Column('id', Integer, primary_key=True)
    start_ip = Column('start_ip', String(40), nullable=False)
    netmask = Column('netmask', String(50), nullable=False)


class User(Base):

    __tablename__ = 'user'

    id = Column('id', Integer, primary_key=True)
    account_id = Column('account_id', Integer, nullable=False)
    username = Column('username', String(16), unique=True, nullable=False)
    password = Column('password', String(100), nullable=False)
    name = Column('name', String(50), nullable=True)
    created = Column('created', Integer, default=unixtime)
