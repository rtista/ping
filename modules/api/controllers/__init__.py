# Local Imports
from .health import HealthCheck
from .account import AccountController
from .user import UserController

# The base point for each route
BASE_ENDPOINT ='/api'

# Declare all your routes here
ROUTES = {

    # Health Module
    '/health': HealthCheck,
}
