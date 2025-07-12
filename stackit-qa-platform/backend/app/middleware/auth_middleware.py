from flask import request, g, jsonify, abort
import jwt
from app.models import User
from flask import current_app
from functools import wraps

def register_auth_middleware(app):
    """
    Register authentication middleware to extract user from JWT
    """
    @app.before_request
    def authenticate_request():
        # Skip auth for OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            return None
            
        # Skip auth for public endpoints
        public_endpoints = [
            'auth.register', 
            'auth.login',
            'questions.list_questions',
            'questions.get_question',
            'static'
        ]
        
        if request.endpoint in public_endpoints:
            return None
            
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # Let the route handle authentication if needed
        
        token = auth_header.split(' ')[1]
        
        try:
            # Decode JWT token
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            
            # Get user from database
            user = User.query.get(payload['user_id'])
            
            if not user:
                return None
                
            if user.banned:
                return jsonify({"error": "Your account has been banned"}), 403
            
            # Set current user in Flask's g object
            g.user = user
            
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            # Continue without authenticated user
            return None

# Add the missing login_required decorator function
def login_required(f):
    """
    Decorator to require authentication for a route.
    Must be used after the authenticate_request middleware runs.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.get('user'):
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function