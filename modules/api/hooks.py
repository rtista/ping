class DatabaseConnection(object):
    """
    Class for database connection hooks.
    """

    @staticmethod
    def acquire(req, resp, resource, params):
        """
        Acquires a connection and appends it to the resource object.

        Args:
            req: The request object.
            resp: The response object.
            resource: The resource object.
            params: The requests parameters.
        """
        resource.dbconn = resource.dbsession()

    @staticmethod
    def dispose(req, resp, resource):
        """
        Removes the connection object from the resource object, rolling back any faulty transactionss.

        Args:
            req: The request object.
            resp: The response object.
            resource: The resource object.
        """
        # Rollback faulty transactions
        if resp.status not in range(200, 300):
            resource.dbconn.rollback()

        # Clean scoped session object
        resource.dbsession.remove()
