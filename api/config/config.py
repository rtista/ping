# Batteries
from os.path import dirname, realpath

# Project base directory
BASE_DIR = realpath(dirname(realpath(__file__)) + '/../')


class Config:
    '''
    Configuration class to hold all configurations for the API.
    '''
    # Application name
    APP_NAME = 'Ping'

    # Debugging Mode
    DEBUG = True

    # Pidfile
    PIDFILE = f'{BASE_DIR}/ping-api.pid'

    # Logging confgurations
    LOG_FILE = f'{BASE_DIR}/ping-api.log'
    LOG_LEVEL = 0


class DevelopmentConfig(Config):
    '''
    Configuration for the development environment.
    '''
    # Debugging Mode
    DEBUG = True

    # Server listening config
    BIND = {
        'host': '0.0.0.0',
        'port': 8000
    }

    # ActiveMQ connection configuration
    MYSQL = {
        'engine': 'mysql+mysqldb',
        'username': 'user',
        'password': 'password',
        'host': '127.0.0.1',
        'port': 3306,
        'dbname': 'ping'
    }
    
    # Token lifetime is 3 hours
    TOKEN_LIFE = 10800


class StagingConfig(Config):
    '''
    Configuration for the staging environment.
    '''
    # Debugging Mode
    DEBUG = True
    
    # Token lifetime is 2 hours
    TOKEN_LIFE = 7200

    # Pidfile
    PIDFILE = '/var/run/ping-api.pid'


class ProductionConfig(Config):
    '''
    Configuration for the production environment.
    '''
    # Debugging Mode
    DEBUG = False
    
    # Token lifetime is 1 hour
    TOKEN_LIFE = 3600

    # Pidfile
    PIDFILE = '/var/run/ping-api.pid'