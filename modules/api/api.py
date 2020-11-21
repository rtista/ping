# Third-party imports
import bjoern
import falcon
import sqlalchemy
import contextlib
from loguru import logger

# Local Imports
from config import Config
from shared.process import UnixProcess
from .middleware import LoggingMiddleware, DatabaseConnectionMiddleware
from .controllers import BASE_ENDPOINT, ROUTES


class PingAPI(UnixProcess):
    """
    The API is the main entrypoint for the application.

    Args:
        shared.process.UnixProcess (class): The UnixProcess class.
    """

    def __init__(self, bind='127.0.0.1', port=8000):
        """
        Create an instance of the Ping API entrypoint process.

        Args:
            bind (str, optional): The bind address for the API process. Defaults to '127.0.0.1'.
            port (int, optional): The port to which to bind. Defaults to 8000.
        """
        UnixProcess.__init__(self, name=f'ping-api :: {port}')
        self._bind = bind
        self._port = port

    @logger.catch
    def run(self):
        """
        This will run in a separate thread.
        """
        # Set proc name
        self.setprocname()

        # Setup database connection
        engine = sqlalchemy.create_engine(
            Config.get('datastore'), poolclass=sqlalchemy.pool.QueuePool, pool_size=5, max_overflow=0)
        session_factory = sqlalchemy.orm.sessionmaker(bind=engine)
        scoped_session = sqlalchemy.orm.scoped_session(session_factory)

        # Create WSGI Application
        api = falcon.API(
            middleware=[
                LoggingMiddleware(),
                DatabaseConnectionMiddleware(scoped_session)
            ]
        )

        # Route Loading
        for route in ROUTES:
            api.add_route(f'{BASE_ENDPOINT}{route}', ROUTES[route]())

        # Start WSGI server
        try:
            logger.info(f'Starting bjoern server on {self._bind}:{self._port}')
            bjoern.run(api, self._bind, self._port)
        except Exception as e:
            logger.info(f'Shutting down bjoern due to: {str(e)}')

        # Dispose all database connection
        with contextlib.suppress(Exception):
            engine.dispose()
