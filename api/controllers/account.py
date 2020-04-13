from models import Account,User
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError

import falcon
from loguru import logger


class AccountController:

    def on_post(self, req, resp):
        """
        Handle POST requests.
        """
        account_name = req.media.get('name')
        username = req.media.get('username')
        password = req.media.get('password')

        # Check if parameters not empty
        if None in [account_name, username, password]:
            resp.media = {'error': 'Invalid Parameters'}
            resp.status_code = falcon.HTTP_400
            return

            # Hash user password
        hashed = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

        account = Account(name=account_name)

        self.db_conn.add(account)

        # Attempt database changes commit
        try:
            # Create Account
            self.db_conn.commit()

            # Now create main user for account
            user = User(account_id=account.account_id, username=username, password=hashed)

            self.db_conn.add(user)

            self.db_conn.commit()

        except SQLAlchemyError as e:

            # Remove Changes
            self.db_conn.rollback()

            # Send error
            logger.error('Message: {}'.format(str(e)))
            raise falcon.HTTPInternalServerError('Internal Server Error', 'Message: {}'.format(str(e)))

        resp.media = {'success': 'account_created'}
        resp.status_code = falcon.HTTP_201