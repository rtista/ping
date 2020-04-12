# Third-party imports
import bjoern
import falcon
from loguru import logger
from setproctitle import setproctitle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models import Base

# Batteries
import os
import sys
import multiprocessing
from datetime import timedelta

# Local Imports
from config import AppConfig
from middleware import LoggingMiddleware, MySQLConnectionMiddleware
from controllers import BASE_ENDPOINT, ROUTES
from sqlalchemy.exc import OperationalError


class PingAPI(multiprocessing.Process):
    """
    The API is the main entrypoint for the application.

    Args:
        multiprocessing.Process (class): The Process class.
    """
    def __init__(self, name, host='127.0.0.1', port=8000):
        """
        Create an instance of the API process.

        Args:
            address (str, optional): The bind address for the API process. Defaults to '127.0.0.1'.
            port (int, optional): The port to which to bind. Defaults to 8000.
        """
        super().__init__(name=name)
        self._host = host
        self._port = port

    def _daemonize(self):
        """
        Detaches the process from the lauching session.
        """
        # Fork allows background running
        if os.fork():
            exit(0)

        # Clear the session id to clear the controlling TTY.
        os.setsid()

        # Set the umask so we have access to all files created by the daemon.
        os.umask(0)

        # Shutdown stdin
        with open('/dev/null', 'r') as dev_null:
            os.dup2(dev_null.fileno(), sys.stdin.fileno())

    @logger.catch
    def run(self):
        """
        This will run in a separate thread.
        """
        # Daemonize the process
        self._daemonize()

        # Remove Default handlers
        logger.remove(None)

        # Create logger sink
        logger.add(AppConfig.LOG_FILE, level=AppConfig.LOG_LEVEL, colorize=True, enqueue=True,
            format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> '
                '| <yellow>{process.name: <23}</yellow> | <level>{message}</level> '
                '(<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>)',
            rotation=timedelta(days=1), retention=timedelta(days=7), compression='tar.gz')

        # Set proc name
        setproctitle(self.name)

        # Write PID file
        with open(AppConfig.PIDFILE, 'w+') as pidfile:
            pidfile.write(str(os.getpid()))

        # MySQL Connection Configuration
        engine = create_engine(
            '{engine}://{username}:{password}@{host}:{port}/{dbname}'.format(**AppConfig.MYSQL)
        )

        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)

        # MySQL Table Models Configuration
        try:
            Base.metadata.create_all(engine)

        except (OperationalError) as e:
            logger.error(f'Operational Error\nCode: {e.orig.args[0]}\nMessage: {e.orig.args[1]}')
            exit(1)

        # Falcon API Configuration
        # Create WSGI Application
        api = falcon.API(
            middleware=[
                LoggingMiddleware(),
                MySQLConnectionMiddleware(Session)
            ]
        )

        # Route Loading
        for route in ROUTES:
            api.add_route(f'{BASE_ENDPOINT}{route}', ROUTES[route]())

        # Start WSGI server
        logger.info(f'Starting bjoern server on {self._host}:{self._port}')

        # Run Bjoern Server
        try:
            bjoern.run(api, self._host, self._port)

        except KeyboardInterrupt:
            logger.info('Bjoern Process terminating...')

        finally:
            # Remove pid file
            os.unlink(AppConfig.PIDFILE)
