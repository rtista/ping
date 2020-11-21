# Batteries
import json
import os
from functools import reduce

# Third-party Imports
import jsonschema
from loguru import logger

# Local Imports
from shared.utils import keyreplace, DefaultValidatingDraft7Validator


class InvalidConfiguration(Exception):
    """
    Thrown when the read configuration is missing
    mandatory parameters or is an invalid JSON format.

    Args:
        builtins.Exception (class): Builtin exception class.
    """
    ...


class Config(object):
    """
    Base configuration class. Reads data from config.json file
    and allows retrieving that data.

    Configurations are cached in memory for faster access.

    Args:
        builtins.object (class): Builtin object class.
    """
    # Base directory
    BASE_DIR = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))

    # Default configuration file
    CONFIG_FILE_PATH = f'config.json'

    # Configuration Syntax
    CONFIG_FILE_SYNTAX = {
        'type': 'object',
        'properties': {
            'log': {
                'type': 'object',
                'properties': {
                    'level': {
                        'type': 'string',
                        'enum': ['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL'],
                        'default': 'DEBUG'
                    },
                    'file': {'type': 'string', 'default': 'logs/ping.log'},
                    'error': {'type': 'string', 'default': 'logs/ping-error.log'}
                },
                'required': ['file', 'error', 'level']
            },
            'pidfile': {'type': 'string', 'default': 'ping.pid'},
            'datastore': {'type': 'string'}
        }
    }

    # Class parameters
    _configfile = None
    _configdict = None

    @classmethod
    def getconfigpath(cls):
        """
        Returns the configuration file path.

        Returns:
            str: The configuration file path.
        """
        return cls._configfile

    @classmethod
    def validate(cls, path):
        """
        Validates the configuration file syntax.

        Args:
            path (str): The path for the configuration file.
        """
        try:
            # Open file and read configuration into memory
            with open(path, 'r') as configfile:
                configdict = json.load(configfile)

            # Replace key dashes with underscores
            configdict = keyreplace(configdict, '-', '_')

            # Validate configuration JSON
            DefaultValidatingDraft7Validator(cls.CONFIG_FILE_SYNTAX).validate(configdict)

            # Return configuration
            return configdict

        except FileNotFoundError:
            raise InvalidConfiguration(f'Configuration file {path} does not exist.')

        except json.JSONDecodeError:
            raise InvalidConfiguration('Configuration file contains invalid JSON format.')

        except jsonschema.ValidationError as e:
            raise InvalidConfiguration(f'Configurations file contains errors: {str(e)}')

    @classmethod
    def load(cls, path):
        """
        Loads the configuration file into memory.

        Args:
            path (str): The path for the configuration file.
        """
        # Set configuration file
        cls._configfile = path

        # Validate and load configuration
        cls._configdict = cls.validate(path)

    @classmethod
    def reload(cls):
        """
        Reloads the configuration file into memory.
        """
        try:
            cls.load(cls._configfile)
        except InvalidConfiguration as e:
            logger.warning(f'Invalid configurations, not reloading. Error: {str(e)}')
            return False

        return True

    @classmethod
    def get(cls, key, default=None):
        """
        Retrieves the value for a key from the configuration file.

        Args:
            key (str): The key from which to get the value. These
                can be several splitted by a dot.
            default (object): What to return if the key is not found.

        Returns:
            object: The configuration value.
        """
        # Retrieve configurations if not loaded
        if not cls._configdict:
            raise InvalidConfiguration('Configurations have not yet been loaded.')

        try:
            value = reduce(dict.get, key.replace('-', '_').split('.'), cls._configdict)
        except TypeError:
            return default

        return default if value is None else value

    @classmethod
    def getpath(cls, key):
        """
        Utility function to retrieve a key whose value is a
        filesystem path. This will read both absolute and
        relative paths and always return an absolute path.

        If relative, the path will be prefixed with the
        project's root.

        Args:
            key (str): The key from which to get the value. These
                can be several splitted by a dot.

        Returns:
            str: The absolute path.
        """
        # Read path from configuration
        path = str(cls.get(key))

        # Prevent empty value
        if not path:
            return None

        # Return path or absolute path from base dir
        return path if os.path.isabs(path) else f'{cls.BASE_DIR}/{path}'
