from flask import Blueprint, request, jsonify, current_app
import jwt
from datetime import datetime, timedelta
from app import db
from app.models import User
from app.utils.validators import validate_registration, validate_login
from app.services.auth_service import authenticate_user, register_user

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate request data
    errors = validate_registration(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    try:
        # Check if username or email already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already taken"}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already registered"}), 409
        
        # Create new user
        user = register_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        # Generate JWT token
        token = generate_token(user)
        
        return jsonify({
            "message": "Registration successful",
            "user": user.to_dict(),
            "token": token
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate a user and return a token"""
    data = request.get_json()
    
    # Validate request data
    errors = validate_login(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Authenticate user
    user = authenticate_user(data.get('username'), data.get('password'))
    
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    if user.banned:
        return jsonify({"error": "Your account has been banned"}), 403
    
    # Generate JWT token
    token = generate_token(user)
    
    return jsonify({
        "message": "Login successful",
        "user": user.to_dict(),
        "token": token
    })

def generate_token(user):
    """Generate a JWT token for the user"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    
    return jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )