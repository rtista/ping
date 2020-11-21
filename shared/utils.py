# Third-party imports
from loguru import logger
from jsonschema import validators, Draft7Validator


class StreamToLogger(object):
    """
    A stream which logs its input into a loguru sink.

    Args:
        builtins.object (class): Default base object class.
    """

    def __init__(self, level="INFO"):
        """
        Creates the StreamToLogger instance.

        Args:
            level (str, optional): The level of luguru logging to use. Defaults to "INFO".
        """
        self._level = level

    def write(self, buffer):
        """
        Writes buffer contents into as log messages.

        Args:
            buffer ([type]): The buffer.
        """
        for line in buffer.rstrip().splitlines():
            logger.log(self._level, line.rstrip())

    def flush(self):
        """
        Override default behavior.
        """
        pass


def keyreplace(obj, old, new):
    """
    Replaces all 'old' occurrences in 'obj' keys with 'new'.

    Args:
        obj (dict): The dictionary of which keys should be modified.
        old (str): The occurrence to be replaced.
        new (str): The occurrence to replace.

    Returns:
        dict: The dict after key replacement.
    """
    # Convert dictionaries keys and values
    if isinstance(obj, dict):
        return {key.replace(old, new): keyreplace(val, old, new) for key, val in obj.items()}

    # Convert array values
    elif isinstance(obj, list):
        return [keyreplace(val, old, new) for val in obj]

    else:
        return obj


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(validator, properties, instance, schema):
            yield error

    return validators.extend(validator_class, {"properties": set_defaults})


DefaultValidatingDraft7Validator = extend_with_default(Draft7Validator)
