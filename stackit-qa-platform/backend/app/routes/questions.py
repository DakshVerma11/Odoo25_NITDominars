from flask import Blueprint, request, jsonify, current_app, g
from ..models.question import Question
from ..models.tag import Tag
from ..services.question_service import QuestionService
from ..utils.validators import validate_question
from ..utils.image_handler import save_uploaded_image
from ..middleware.auth_middleware import login_required
import bleach

questions_bp = Blueprint('questions', __name__)
question_service = QuestionService()

# Allowed HTML tags and attributes for rich text
ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 's', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'blockquote', 'ul', 'ol', 'li', 'a', 'img', 'div', 'span']
                
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'width', 'height'],
    'div': ['style', 'class', 'align'],
    'span': ['style', 'class'],
    '*': ['style', 'class']
}

ALLOWED_STYLES = ['text-align']

def sanitize_html(content):
    """Sanitize HTML content to prevent XSS attacks"""
    return bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        styles=ALLOWED_STYLES,
        strip=True
    )

@questions_bp.route('', methods=['GET'])
def get_questions():
    """Get all questions with pagination"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    tag = request.args.get('tag')
    search = request.args.get('search')
    
    questions, total = question_service.get_questions(
        page=page, 
        per_page=per_page,
        tag=tag,
        search=search
    )
    
    return jsonify({
        'questions': [q.to_dict() for q in questions],
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })

@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """Get a specific question with its answers"""
    question = question_service.get_question_by_id(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    return jsonify(question_service.get_question_details(question))

@questions_bp.route('', methods=['POST'])
@login_required
def create_question():
    """Create a new question with rich text content"""
    data = request.json
    
    # Validate input
    validation_errors = validate_question(data)
    if validation_errors:
        return jsonify({'errors': validation_errors}), 400
    
    # Sanitize HTML content
    data['description'] = sanitize_html(data['description'])
    
    # Create question
    question = question_service.create_question(
        user_id=g.user.id,
        title=data['title'],
        description=data['description'],
        tags=data.get('tags', [])
    )
    
    return jsonify(question.to_dict()), 201

@questions_bp.route('/<int:question_id>', methods=['PUT'])
@login_required
def update_question(question_id):
    """Update an existing question"""
    data = request.json
    question = question_service.get_question_by_id(question_id)
    
    if not question:
        return jsonify({'error': 'Question not found'}), 404
        
    # Check ownership
    if question.user_id != g.user.id and not g.user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Validate input
    validation_errors = validate_question(data)
    if validation_errors:
        return jsonify({'errors': validation_errors}), 400
    
    # Sanitize HTML content
    if 'description' in data:
        data['description'] = sanitize_html(data['description'])
    
    # Update question
    updated_question = question_service.update_question(
        question_id=question_id,
        title=data.get('title'),
        description=data.get('description'),
        tags=data.get('tags')
    )
    
    return jsonify(updated_question.to_dict())

@questions_bp.route('/upload-image', methods=['POST'])
@login_required
def upload_image():
    """Handle image uploads for rich text editor"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
        
    file = request.files['image']
    
    if not file.filename:
        return jsonify({'error': 'No image selected'}), 400
    
    try:
        image_url = save_uploaded_image(file)
        return jsonify({'imageUrl': image_url})
    except Exception as e:
        current_app.logger.error(f"Image upload error: {str(e)}")
        return jsonify({'error': 'Failed to upload image'}), 500