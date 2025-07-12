import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file):
    """
    Validate an uploaded image file
    
    Args:
        file: File object from request.files
        
    Returns:
        dict: Empty if valid, or containing error message
    """
    if file is None:
        return {"error": "No file provided"}
    
    if not allowed_file(file.filename):
        return {"error": f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"}
    
    if file.content_length and file.content_length > MAX_FILE_SIZE:
        return {"error": f"File too large. Maximum size: {MAX_FILE_SIZE // 1024 // 1024}MB"}
    
    return {}

def save_image(file, subfolder="uploads"):
    """
    Save an uploaded image with a unique filename
    
    Args:
        file: File object from request.files
        subfolder: Directory within UPLOAD_FOLDER to save the file
        
    Returns:
        str: Path to the saved file (relative to static directory)
    """
    try:
        # Create a unique filename
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        unique_filename = f"{name}_{uuid.uuid4().hex}{ext}"
        
        # Ensure upload directory exists
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file path
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save the file
        file.save(file_path)
        
        # Optimize image if it's not a GIF
        if ext.lower() != '.gif':
            optimize_image(file_path)
        
        # Return the path relative to static directory
        return os.path.join(subfolder, unique_filename)
    
    except Exception as e:
        current_app.logger.error(f"Image save error: {str(e)}")
        return None

def optimize_image(file_path, max_width=1200):
    """
    Optimize an image by resizing and compressing
    
    Args:
        file_path: Path to the image file
        max_width: Maximum width to resize to
    """
    try:
        img = Image.open(file_path)
        
        # Resize if width exceeds max_width
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.LANCZOS)
        
        # Save with optimized quality
        img.save(file_path, optimize=True, quality=85)
        
    except Exception as e:
        current_app.logger.error(f"Image optimization error: {str(e)}")