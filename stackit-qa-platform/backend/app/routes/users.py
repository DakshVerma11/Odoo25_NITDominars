from flask import Blueprint, request, jsonify, g, abort
from app import db
from app.models import User, Question, Answer
from app.utils.decorators import login_required
from app.utils.validators import validate_user_update

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """Get current user's profile"""
    return jsonify(g.user.to_dict(include_email=True))

@users_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """Update current user's profile"""
    data = request.get_json()
    
    # Validate request data
    errors = validate_user_update(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    try:
        # Check if email is being updated and it's not already taken
        if 'email' in data and data['email'] != g.user.email:
            if User.query.filter_by(email=data['email']).first():
                return jsonify({"error": "Email already in use"}), 409
            g.user.email = data['email']
        
        # Update password if provided
        if 'password' in data and data['password']:
            g.user.set_password(data['password'])
        
        db.session.commit()
        return jsonify({"message": "Profile updated successfully", "user": g.user.to_dict(include_email=True)})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@users_bp.route('/<string:username>', methods=['GET'])
def get_user_profile(username):
    """Get a user's public profile"""
    user = User.query.filter_by(username=username).first_or_404()
    
    # Count user's questions and answers
    question_count = Question.query.filter_by(user_id=user.id).count()
    answer_count = Answer.query.filter_by(user_id=user.id).count()
    
    # Get recent activity (last 5 questions and answers)
    recent_questions = [q.to_dict() for q in Question.query.filter_by(user_id=user.id)
                        .order_by(Question.created_at.desc()).limit(5).all()]
    
    recent_answers = [a.to_dict() for a in Answer.query.filter_by(user_id=user.id)
                     .order_by(Answer.created_at.desc()).limit(5).all()]
    
    return jsonify({
        "user": user.to_dict(),
        "stats": {
            "question_count": question_count,
            "answer_count": answer_count
        },
        "recent_activity": {
            "questions": recent_questions,
            "answers": recent_answers
        }
    })

@users_bp.route('/<string:username>/questions', methods=['GET'])
def get_user_questions(username):
    """Get all questions asked by a user"""
    user = User.query.filter_by(username=username).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    questions_page = Question.query.filter_by(user_id=user.id)\
        .order_by(Question.created_at.desc())\
        .paginate(page=page, per_page=per_page)
    
    return jsonify({
        "questions": [q.to_dict() for q in questions_page.items],
        "total": questions_page.total,
        "page": page,
        "pages": questions_page.pages,
        "per_page": per_page
    })

@users_bp.route('/<string:username>/answers', methods=['GET'])
def get_user_answers(username):
    """Get all answers provided by a user"""
    user = User.query.filter_by(username=username).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    answers_page = Answer.query.filter_by(user_id=user.id)\
        .order_by(Answer.created_at.desc())\
        .paginate(page=page, per_page=per_page)
    
    return jsonify({
        "answers": [a.to_dict() for a in answers_page.items],
        "total": answers_page.total,
        "page": page,
        "pages": answers_page.pages,
        "per_page": per_page
    })