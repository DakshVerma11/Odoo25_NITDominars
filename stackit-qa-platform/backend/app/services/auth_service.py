from app import db
from app.models import User

def authenticate_user(username, password):
    """
    Authenticate a user by username and password
    
    Args:
        username: The username to check
        password: The plaintext password to verify
        
    Returns:
        User object if authentication successful, None otherwise
    """
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        return user
    
    return None

def register_user(username, email, password, role='user'):
    """
    Register a new user
    
    Args:
        username: The username for the new user
        email: The email for the new user
        password: The plaintext password to hash and store
        role: The user role (default 'user')
        
    Returns:
        Newly created User object
    """
    user = User(
        username=username,
        email=email,
        role=role
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    return user