from flask import Blueprint, request, jsonify, g
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from ..services.question_service import QuestionService
from ..utils.image_handler import save_uploaded_image
from ..middleware.auth_middleware import login_required
from ..utils.validators import validate_question

# Define the blueprint with a proper URL prefix
questions_bp = Blueprint('questions', __name__, url_prefix='/api/questions')

# Fix routes to ensure all start with a leading slash
@questions_bp.route('/', methods=['GET'])  # Fixed: added leading slash
def list_questions():
    """Get a list of questions with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 50)
    tag = request.args.get('tag')
    search = request.args.get('search')
    
    try:
        result = QuestionService.get_questions(
            page=page, 
            per_page=per_page,
            tag=tag,
            search=search
        )
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error fetching questions: {str(e)}")
        return jsonify({"error": "Failed to fetch questions"}), 500

@questions_bp.route('/<int:question_id>', methods=['GET'])  # Fixed: added leading slash
def get_question(question_id):
    """Get a specific question by ID"""
    try:
        question = QuestionService.get_question_by_id(question_id)
        if not question:
            return jsonify({"error": "Question not found"}), 404
            
        return jsonify(question.to_dict(with_answers=True))
    except Exception as e:
        current_app.logger.error(f"Error fetching question: {str(e)}")
        return jsonify({"error": "Failed to fetch question"}), 500

@questions_bp.route('/', methods=['POST'])  # Fixed: added leading slash
@login_required
def create_question():
    """Create a new question"""
    data = request.form.to_dict()
    tags = request.form.getlist('tags')
    if tags:
        data['tags'] = tags
    
    # Validate input
    errors = validate_question(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Handle image upload if present
    image_url = None
    if 'image' in request.files:
        image = request.files['image']
        if image.filename:
            image_url = save_uploaded_image(image, 'questions')
    
    try:
        question = QuestionService.create_question(
            user_id=g.user.id,
            title=data['title'],
            description=data['description'],
            tags=data.get('tags', [])
        )
        
        return jsonify(question.to_dict()), 201
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error creating question: {str(e)}")
        return jsonify({"error": "Failed to create question"}), 500
    except Exception as e:
        current_app.logger.error(f"Error creating question: {str(e)}")
        return jsonify({"error": "Failed to create question"}), 500

# Make sure all other routes have leading slashes too