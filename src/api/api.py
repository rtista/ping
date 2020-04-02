import falcon
import bjoern

from routes import BASE_ENDPOINT, ROUTES
from resources.health_check import HealthCheck


def create():
    api = falcon.API()

    for route in ROUTES:
        api.add_route(f"{BASE_ENDPOINT}{route}", ROUTES[route]())

    # Add Health Check
    api.add_route("/", HealthCheck())
    return api


if __name__ == '__main__':
    api = create()

    HOST = '127.0.0.1'
    PORT = 8000
    print(f'Starting bjoern server on {HOST}:{PORT}')
    bjoern.listen(api, HOST, PORT)
    bjoern.run()

