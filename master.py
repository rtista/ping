# Batteries
import contextlib
import os
import signal
import time
from datetime import timedelta

# Third-party
from loguru import logger

# Local imports
from config import Config
from modules.api import PingAPI
from shared.process import UnixProcess


class PingMaster(UnixProcess):
    """
    The ping master process will monitor and manage its children.

    Args:
        shared.process.UnixProcess (class): UnixProcess class.
    """

    def __init__(self, configpath):
        """
        Creates the main process.

        Args:
            configpath (str): The configuration file path.
        """
        super().__init__('master process')
        self._configpath = configpath
        self._children = []

    @staticmethod
    def _loadchildren():
        """
        Loads children from configuration into process map.

        Raises:
            InvalidConfiguration: On invalid configurations.

        Returns:
            list: Configured children list.
        """
        return [
            [PingAPI, {}, None],
        ]

    def _monit(self):
        """
        Monitors the instances of running processes.
        """
        # For each children
        for index, (cls, kwargs, proc) in enumerate(self._children):

            # Spawn children if required
            if proc is None:

                try:
                    self._children[index][2] = cls(**kwargs)
                    self._children[index][2].start()
                except Exception as e:
                    self._children.pop(index)
                    logger.error(f'Could not instantiate/spawn child \'{cls.__name__}\' due to: {str(e)}')
                    logger.info(f'Removed child \'{cls.__name__}\' from processes list.')

            elif not (proc.is_alive() or proc.exitcode is None):

                # Join process and delete instance
                proc.join(timeout=0.1)
                self._children[index][2] = None

    @logger.catch
    def run(self):
        """
        This will run in a separate process.
        """
        # Daemonize
        self.daemonize()

        # Create helper sink
        logger.add(
            Config.getpath('log.file'),
            level=Config.get('log.level'), colorize=True, enqueue=True,
            format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> |'
                   '<yellow>{process.name: <23}</yellow> | '
                   '<level>{message}</level> (<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>)',
            rotation=timedelta(days=1), retention=timedelta(days=30), compression='gz')

        # Set process title
        self.setprocname()

        # Set signal handlers
        # self.sigreg(signal.SIGHUP, self._reload)
        self.sigreg(signal.SIGINT, self.sighandler)
        self.sigreg(signal.SIGTERM, self.sighandler)

        # Write PID file
        with open(Config.getpath('pidfile'), 'w+') as pidfile:
            pidfile.write(str(os.getpid()))

        # Load children processes
        self._children = self._loadchildren()

        # While not stopping
        while self._stop is False:
            # Monit instances
            self._monit()

            time.sleep(1)

        logger.debug('Terminating...')

        # Stop all children whose instance is not None
        children = [proc for _, _, proc in self._children if proc]

        # While children have not stopped
        while children:

            for index, proc in enumerate(children):

                logger.debug(f'Terminating child: {proc.name} with pid {proc.pid}...')

                # Send SIGTERM to child process
                os.kill(proc.pid, signal.SIGINT if isinstance(proc, PingAPI) else signal.SIGTERM)

                # On join fail, SIGKILL child process
                proc.join(timeout=1)

                # If child has not stopped, give it time
                if proc.is_alive() or proc.exitcode is None:
                    continue

                # Remove children
                children.pop(index)

        # Remove pidfile and socket
        with contextlib.suppress(FileNotFoundError):
            os.unlink(Config.getpath('pidfile'))
