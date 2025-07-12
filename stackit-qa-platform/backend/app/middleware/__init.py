# Initialize middleware package
from . import auth_middleware
from . import cors_middleware
from . import error_handler

def register_middleware(app):
    """
    Register all middleware with the Flask application
    """
    # Register error handlers
    error_handler.register_error_handlers(app)
    
    # Register CORS middleware
    cors_middleware.configure_cors(app)
    
    # Register authentication middleware
    auth_middleware.register_auth_middleware(app)