#!/bin/python3

# Third-party imports
from loguru import logger

# Batteries
import os
import time
from signal import SIGINT
from argparse import ArgumentParser

# Own Imports
from config import AppConfig
from api import PingAPI


def stop():
    """
    Stops the ping api process.
    """
    # Check for pidfile
    if not os.path.isfile(AppConfig.PIDFILE):
        print('Could not find pidfile. Is the process running?')
        exit(0)

    # Read Ping API PID from pidfile
    with open(AppConfig.PIDFILE, 'r') as pidfile:
        pid = int(pidfile.readline())

    # Check for running pid
    if not os.path.isdir(f'/proc/{pid}'):
        print('Process is not running. Removing stale pidfile.')
        exit(0)

    # Send SIGTERM to process
    os.kill(pid, SIGINT)

    # Wait for process to end
    while os.path.isdir(f'/proc/{pid}'):
        print('Waiting for ping to stop...')
        time.sleep(1)


def start():
    """
    Starts the ping supervisor process.
    """
    # Check for pidfile existence
    if os.path.isfile(AppConfig.PIDFILE):

        # Check for stale PID file
        with open(AppConfig.PIDFILE, 'r') as pidfile:

            pid = pidfile.read()

            # Check if process with PID is running
            if os.path.isdir(f'/proc/{pid}'):
                print(f'Unable to start. Process already running with pid {pid}')
                exit(0)

        # Remove stale PID file
        print(f'Found stale pid file at {AppConfig.PIDFILE}. Removing...')
        os.unlink(AppConfig.PIDFILE)

    # Start the ping master process
    PingAPI('ping-api', **AppConfig.BIND).start()


def restart():
    """
    Restarts the ping supervisor process.
    """
    stop()
    start()

# Available operations
OPERATIONS = {
    'stop': stop,
    'start': start,
    'restart': restart
}

# Main
if __name__ == '__main__':

    # Create argument parser
    parser = ArgumentParser(description='ping MTA Controller')
    parser.add_argument('operation', type=str,
                        help=f'The operation to execute. Possible values: {", ".join(OPERATIONS.keys())}',
                        choices=OPERATIONS.keys())

    # Parse Arguments
    args = parser.parse_args()

    # Execute requested operation
    try:
        OPERATIONS[args.operation]()

    except Exception as e:
        print(f'Error on operation: {str(e)}')
        exit(1)
