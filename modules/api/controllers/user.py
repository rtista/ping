# Third-party Imports
import falcon
from loguru import logger
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError

# Local Imports
from shared.models import User


class UserController(object):
    """
    Represents the User REST resource.
    
    Args:
        object (class): Base native object class.
    """
    def on_post(self,req,resp):
        """
        Handle POST requests.
        """
        username = req.media.get('username')
        password = req.media.get('password')

        # Check if parameters not empty
        if None in (username, password):
            raise falcon.HTTPBadRequest('Bad Request', 'Invalid Parameters')

        # Hash user password
        hashed = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

        # Now create main user for account
        user = User(username=username, password=hashed)

        self.db_conn.add(user)

        # Attempt database changes commit
        try:
            # Create User
            self.db_conn.commit()

        except SQLAlchemyError as e:

            # Rollback Changes
            self.db_conn.rollback()

            # Send error
            logger.error(f'Database Error: (Code: {e.orig.args[0]} Message: {e.orig.args[1]})')
            raise falcon.HTTPInternalServerError('Internal Server Error', 'An error ocurred while communicating with the database.')

        resp.media = {'success': 'user_created'}
        resp.status = falcon.HTTP_201
