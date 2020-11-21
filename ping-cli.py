#!/usr/bin/python3

# Batteries
import os
import signal
import time
from argparse import ArgumentParser

# Third-party Imports
import sqlalchemy

# Local Imports
from config import Config, InvalidConfiguration
from shared.models import Base


def stop():
    """
    Stops the ping main process.

    Returns:
        int: The exit code to exit with.
    """
    # Check for pidfile
    if not os.path.isfile(Config.getpath('pidfile')):
        print('Could not find pidfile. Is the process running?')
        return 0

    # Read Supervisor PID from pidfile
    with open(Config.getpath('pidfile'), 'r') as pidfile:
        pid = int(pidfile.readline())

    # Check for running pid
    if not os.path.isdir(f'/proc/{pid}'):

        # Remove pidfile
        os.unlink(Config.getpath('pidfile'))

        # Also remove socket file if existent
        if os.path.isfile(Config.getpath('socket')):
            os.unlink(Config.getpath('socket'))

        print('Process is not running. Removed stale pidfile and socket.')

        return 0

    # Send SIGTERM to process
    os.kill(pid, signal.SIGTERM)

    # Wait for process to end
    while os.path.isdir(f'/proc/{pid}'):
        print('Waiting for Ping to stop...')
        time.sleep(1)

    return 0


def start():
    """
    Starts the Ping main process.

    Returns:
        int: The exit code to exit with.
    """
    # Check for pidfile existence
    if os.path.isfile(Config.getpath('pidfile')):

        # Check for stale PID file
        with open(Config.getpath('pidfile'), 'r') as pidfile:

            pid = pidfile.read()

            # Check if process with PID is running
            if os.path.isdir(f'/proc/{pid}'):
                print(f'Unable to start. Process already running with pid {pid}.')
                return 1

        # Remove stale PID file
        print(f'Found stale pid file at {Config.get("pidfile")}. Removing...')
        os.unlink(Config.getpath('pidfile'))

        # Remove stale socket if existent
        if os.path.isfile(Config.getpath('socket')):
            os.unlink(Config.getpath('socket'))

    # Only import master when required
    from master import PingMaster

    # Create and start the Ping master process
    PingMaster(Config.getconfigpath()).start()

    return 0


def restart():
    """
    Restarts the Ping supervisor process.

    Returns:
        int: The exit code to exit with.
    """
    # Save exitcode from stop execution
    exitcode = stop()

    # Start only if stop returns successfuly
    if exitcode == 0:
        exitcode = start()

    return exitcode


def status():
    """
    Checks if the Ping process is running.

    Returns:
        int: The exit code to exit with.
    """
    # Check for pidfile existence
    if os.path.isfile(Config.getpath('pidfile')):

        # Check for stale PID file
        with open(Config.getpath('pidfile'), 'r') as pidfile:

            pid = pidfile.read()

            # Check if process with PID is running
            if os.path.isdir(f'/proc/{pid}'):
                print(f'Ping process is running with pid {pid}.')
                return 0

        # Remove stale PID file
        print(f'Found stale pid file at {Config.get("pidfile")}. Removing...')
        os.unlink(Config.getpath('pidfile'))

    print('Ping process is not running.')
    return 1


def _reload():
    """
    Signal the Ping master to reload configurations.

    Returns:
        int: The exit code to exit with.
    """
    # Check for pidfile
    if not os.path.isfile(Config.getpath('pidfile')):
        print('Could not find pidfile. Is the process running?')
        return 1

    # Read Supervisor PID from pidfile
    with open(Config.getpath('pidfile'), 'r') as pidfile:
        pid = int(pidfile.readline())

    # Check for running pid
    if not os.path.isdir(f'/proc/{pid}'):
        print('Process is not running. Removing stale pidfile.')
        return 1

    # Send SIGTERM to process
    os.kill(pid, signal.SIGHUP)

    return 0


def validate(path):
    """
    Validates the configuration file syntax.

    Args:
        path (str): The configuration file path.

    Returns:
        int: The exit code to exit with.
    """
    Config.validate(path)


def initdb():
    """
    Creates database tables.

    Returns:
        int: The exit code to exit with.
    """
    # Create engine
    engine = sqlalchemy.create_engine(Config.get('datastore'), poolclass=sqlalchemy.pool.NullPool)

    # Create database schema
    try:
        Base.metadata.create_all(engine)

    except sqlalchemy.exc.OperationalError as e:
        print(f'Operational Error\nCode: {e.orig.args[0]}\nMessage: {e.orig.args[1]}')
        return 1

    return 0


# Available operations
OPERATIONS = {
    'stop': stop,
    'start': start,
    'restart': restart,
    'status': status,
    'reload': _reload,
    'initdb': initdb
}

# Main
if __name__ == '__main__':

    # Create argument parser
    parser = ArgumentParser(description='Ping CLI')
    parser.add_argument('-t', '--test', action="store_true", help=f'Validates the configuration file for errors.')
    parser.add_argument('-c', '--config', type=str, help=f'The configuration file path.',
                        default=Config.CONFIG_FILE_PATH)
    parser.add_argument('operation', type=str, choices=OPERATIONS.keys(),
                        help=f'The operation to execute. Possible values: {", ".join(OPERATIONS.keys())}')

    # Parse Arguments
    args = parser.parse_args()

    # Convert to realpath
    configfile = f'{os.path.realpath(os.path.dirname(os.path.realpath(__file__)))}/{args.config}'

    # Execute requested operation
    try:

        # If test then just validate configuration
        if args.test:
            exit(validate(configfile))

        else:
            # Load Configuration
            Config.load(configfile)

            # Execute Operation
            exit(OPERATIONS[args.operation]())

    except InvalidConfiguration as e:

        print(f'Invalid Configuration: {str(e)}')
        exit(1)

    except Exception as e:
        print(f'Unknown error occurred: {str(e)}')
        exit(1)
