# Batteries
import time

# Third-party Imports
from loguru import logger


class LoggingMiddleware(object):
    """
    Log every request made to the server
    """

    @classmethod
    def process_request(cls, req, resp):
        """Process the request before routing it.

        Note:
            Because Falcon routes each request based on req.path, a
            request can be effectively re-routed by setting that
            attribute to a new value from within process_request().

        Args:
            req: Request object that will eventually be
                routed to an on_* responder method.
            resp: Response object that will be routed to
                the on_* responder.
        """
        req.req_start_time = time.time()

    @classmethod
    def process_response(cls, req, resp, resource, req_succeeded):
        """Post-processing of the response (after routing).

        Args:
            req: Request object.
            resp: Response object.
            resource: Resource object to which the request was
                routed. May be None if no route was found
                for the request.
            req_succeeded: True if no exceptions were raised while
                the framework processed and routed the request;
                otherwise False.
        """
        reqtime = round(float(time.time() - req.req_start_time), 3)
        logger.info(f'{req.access_route} {req.method} {req.uri} {resp.status} {req_succeeded} {reqtime}')


class DatabaseConnectionMiddleware(object):
    """
    Shares the database connection amongst all requests.

    Args:
        builtins.object (class): Native object class.
    """

    def __init__(self, session):
        """
        Create the middleware instance.

        Args:
            session (): The scoped session object.
        """
        self._Session = session

    def process_resource(self, req, resp, resource, params):
        """
        Process the request after routing.

        Note:
            This method is only called when the request matches
            a route to a resource.

        Args:
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
            resource: Resource object to which the request was
                routed.
            params: A dict-like object representing any additional
                params derived from the route's URI template fields,
                that will be passed to the resource's responder
                method as keyword arguments.
        """
        resource.dbsession = self._Session
