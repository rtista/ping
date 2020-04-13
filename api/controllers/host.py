# Third-Party
import falcon
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

# Batteries
import sys

# Local Imports
from models import Host


class HostController(object):
    """
    Represents the Host REST resource.
    
    Args:
        object (class): Base native object class.
    """
    def on_get(self, req, resp):
        """
        Handles GET requests by retrieving hosts.
        
        Args:
            req ([type]): The request object.
            resp ([type]): The response object.
        """
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """
        Handles POST requests by creating a host.

        Args:
            req ([type]): The request object.
            resp ([type]): The response object.
        """
        # Check for request body
        if not req.media:
            raise falcon.HTTPBadRequest('Bad Request', 'Could not find request body')

        # Retrieve data from request body
        host_type = req.media.get('type')

        # Validate mandatory data
        if not host_type or host_type.lower() not in ('bm', 'vm', 'ct'):
            raise falcon.HTTPConflict('Conflict', 'Invalid host type')

        # Create new host
        self.db_conn.add(Host(type=host_type))

        # Attempt database changes commit
        try:
            self.db_conn.commit()

        except SQLAlchemyError as e:

            # Rollback Changes
            self.db_conn.rollback()

            logger.error(f'Database Error: (Code: {e.orig.args[0]} Message: {e.orig.args[1]})')

            # Raise error
            raise falcon.HTTPInternalServerError('Internal Server Error', 'An error ocurred while communicating with the database.')
        
        resp.media = {'Message': 'Account created successfuly'}
        resp.status_code = falcon.HTTP_201
