from functools import wraps
from flask import request, g, jsonify, abort
import jwt
from app.models import User
from flask import current_app

def login_required(f):
    """
    Decorator to ensure the user is authenticated
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization required"}), 401
        
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
                return jsonify({"error": "User not found"}), 401
                
            if user.banned:
                return jsonify({"error": "Your account has been banned"}), 403
            
            # Set current user in Flask's g object
            g.user = user
            
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def admin_required(f):
    """
    Decorator to ensure the user is an admin
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First ensure user is logged in
        @login_required
        def check_admin(*args, **kwargs):
            if not g.user.is_admin():
                abort(403, description="Admin access required")
            return f(*args, **kwargs)
        
        return check_admin(*args, **kwargs)
    
    return decorated_function