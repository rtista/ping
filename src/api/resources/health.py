import sys

import ujson
import falcon
from loguru import logger

@logger.catch
class HealthCheck(object):
    def on_get(self, req, resp):
        try:
            resp.body = ujson.dumps({"success": True, "message": "A tua tia de 4"})
            resp.status = falcon.HTTP_200
        except Exception as e:
            logger.warning(f"HEALTHCHECK | {e}")
            resp.body = ujson.dumps({"success": False})
            resp.status = falcon.HTTP_500
