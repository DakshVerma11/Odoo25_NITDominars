from flask import Blueprint, request, jsonify, g, abort
from app import db
from app.models import Question, Tag, question_tags
from app.utils.validators import validate_question
from app.utils.decorators import login_required, admin_required
from app.services.question_service import get_questions, get_question_by_id, create_question
from app.utils.helpers import sanitize_html

questions_bp = Blueprint('questions', __name__, url_prefix='/api/questions')

@questions_bp.route('', methods=['GET'])
def list_questions():
    """Get all questions with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    tag = request.args.get('tag')
    search = request.args.get('search')
    
    questions_data = get_questions(page, per_page, tag, search)
    
    response = jsonify(questions_data)
    response.headers['Cache-Control'] = 'public, max-age=60'
    return response

@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """Get a specific question by ID"""
    question = get_question_by_id(question_id)
    
    if not question:
        abort(404, description="Question not found")
        
    return jsonify(question.to_dict(include_answers=True))

@questions_bp.route('', methods=['POST'])
@login_required
def post_question():
    """Create a new question"""
    data = request.get_json()
    
    # Validate request data
    errors = validate_question(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Sanitize HTML content
    data['description'] = sanitize_html(data['description'])
    
    # Create question
    try:
        question = create_question(
            user_id=g.user.id,
            title=data['title'],
            description=data['description'],
            tags=data.get('tags', [])
        )
        return jsonify(question.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@questions_bp.route('/<int:question_id>', methods=['PUT'])
@login_required
def update_question(question_id):
    """Update an existing question"""
    question = Question.query.get_or_404(question_id)
    
    # Check if user is the author or an admin
    if question.user_id != g.user.id and not g.user.is_admin():
        abort(403, description="Permission denied")
        
    data = request.get_json()
    errors = validate_question(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Sanitize HTML content
    data['description'] = sanitize_html(data['description'])
    
    try:
        # Update question fields
        question.title = data['title']
        question.description = data['description']
        
        # Update tags if provided
        if 'tags' in data:
            # Clear existing tags
            question.tags = []
            
            # Add new tags
            for tag_name in data['tags']:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                question.tags.append(tag)
        
        db.session.commit()
        return jsonify(question.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@questions_bp.route('/<int:question_id>', methods=['DELETE'])
@login_required
def delete_question(question_id):
    """Delete a question"""
    question = Question.query.get_or_404(question_id)
    
    # Check if user is the author or an admin
    if question.user_id != g.user.id and not g.user.is_admin():
        abort(403, description="Permission denied")
    
    try:
        db.session.delete(question)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500