import re
from email_validator import validate_email, EmailNotValidError

def validate_registration(data):
    """
    Validate user registration data
    """
    errors = {}
    
    # Username validation
    if 'username' not in data or not data['username']:
        errors['username'] = 'Username is required'
    elif len(data['username']) < 3:
        errors['username'] = 'Username must be at least 3 characters'
    elif len(data['username']) > 50:
        errors['username'] = 'Username cannot exceed 50 characters'
    elif not re.match(r'^[a-zA-Z0-9_]+$', data['username']):
        errors['username'] = 'Username can only contain letters, numbers, and underscores'
    
    # Email validation
    if 'email' not in data or not data['email']:
        errors['email'] = 'Email is required'
    else:
        try:
            validate_email(data['email'])
        except EmailNotValidError:
            errors['email'] = 'Invalid email format'
    
    # Password validation
    if 'password' not in data or not data['password']:
        errors['password'] = 'Password is required'
    elif len(data['password']) < 8:
        errors['password'] = 'Password must be at least 8 characters'
    elif not re.search(r'[A-Z]', data['password']):
        errors['password'] = 'Password must contain at least one uppercase letter'
    elif not re.search(r'[a-z]', data['password']):
        errors['password'] = 'Password must contain at least one lowercase letter'
    elif not re.search(r'[0-9]', data['password']):
        errors['password'] = 'Password must contain at least one number'
    
    return errors

def validate_login(data):
    """
    Validate user login data
    """
    errors = {}
    
    if 'username' not in data or not data['username']:
        errors['username'] = 'Username is required'
    
    if 'password' not in data or not data['password']:
        errors['password'] = 'Password is required'
    
    return errors

def validate_question(data):
    """
    Validate question data
    """
    errors = {}
    
    # Title validation
    if 'title' not in data or not data['title']:
        errors['title'] = 'Title is required'
    elif len(data['title']) < 10:
        errors['title'] = 'Title must be at least 10 characters'
    elif len(data['title']) > 255:
        errors['title'] = 'Title cannot exceed 255 characters'
    
    # Description validation
    if 'description' not in data or not data['description']:
        errors['description'] = 'Description is required'
    elif len(data['description']) < 20:
        errors['description'] = 'Description must be at least 20 characters'
    
    # Tags validation
    if 'tags' not in data or not data['tags']:
        errors['tags'] = 'At least one tag is required'
    elif not isinstance(data['tags'], list):
        errors['tags'] = 'Tags must be a list'
    elif len(data['tags']) > 5:
        errors['tags'] = 'A question cannot have more than 5 tags'
    else:
        for tag in data['tags']:
            if len(tag) < 2 or len(tag) > 50:
                errors['tags'] = 'Tags must be between 2 and 50 characters'
                break
    
    return errors

def validate_answer(data):
    """
    Validate answer data
    """
    errors = {}
    
    # Content validation
    if 'content' not in data or not data['content']:
        errors['content'] = 'Answer content is required'
    elif len(data['content']) < 20:
        errors['content'] = 'Answer must be at least 20 characters'
    
    # Question ID validation
    if 'question_id' not in data or not data['question_id']:
        errors['question_id'] = 'Question ID is required'
    
    return errors