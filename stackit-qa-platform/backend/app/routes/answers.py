from flask import Blueprint, request, jsonify, g, abort
from app import db
from app.models import Answer, Question, Notification
from app.utils.validators import validate_answer
from app.utils.decorators import login_required
from app.services.notification_service import create_notification
from app.utils.helpers import sanitize_html

answers_bp = Blueprint('answers', __name__, url_prefix='/api/answers')

@answers_bp.route('', methods=['POST'])
@login_required
def post_answer():
    """Post a new answer to a question"""
    data = request.get_json()
    
    # Validate request data
    errors = validate_answer(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    question_id = data.get('question_id')
    question = Question.query.get_or_404(question_id)
    
    # Sanitize HTML content
    content = sanitize_html(data['content'])
    
    try:
        # Create new answer
        answer = Answer(
            question_id=question_id,
            user_id=g.user.id,
            content=content
        )
        db.session.add(answer)
        db.session.commit()
        
        # Create notification for question author
        if question.user_id != g.user.id:
            create_notification(
                user_id=question.user_id,
                notification_type='answer',
                source_id=answer.id
            )
        
        return jsonify(answer.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@answers_bp.route('/<int:answer_id>', methods=['PUT'])
@login_required
def update_answer(answer_id):
    """Update an existing answer"""
    answer = Answer.query.get_or_404(answer_id)
    
    # Check if user is the author or an admin
    if answer.user_id != g.user.id and not g.user.is_admin():
        abort(403, description="Permission denied")
        
    data = request.get_json()
    errors = validate_answer(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Sanitize HTML content
    content = sanitize_html(data['content'])
    
    try:
        answer.content = content
        db.session.commit()
        return jsonify(answer.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@answers_bp.route('/<int:answer_id>', methods=['DELETE'])
@login_required
def delete_answer(answer_id):
    """Delete an answer"""
    answer = Answer.query.get_or_404(answer_id)
    
    # Check if user is the author or an admin
    if answer.user_id != g.user.id and not g.user.is_admin():
        abort(403, description="Permission denied")
    
    try:
        db.session.delete(answer)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@answers_bp.route('/<int:answer_id>/accept', methods=['PUT'])
@login_required
def accept_answer(answer_id):
    """Mark an answer as accepted"""
    answer = Answer.query.get_or_404(answer_id)
    question = Question.query.get_or_404(answer.question_id)
    
    # Only the question author can accept an answer
    if question.user_id != g.user.id:
        abort(403, description="Only the question author can accept an answer")
    
    try:
        # Reset any previously accepted answer for this question
        previously_accepted = Answer.query.filter_by(
            question_id=question.id, accepted=True
        ).first()
        
        if previously_accepted:
            previously_accepted.accepted = False
        
        # Mark this answer as accepted
        answer.accepted = True
        db.session.commit()
        
        return jsonify(answer.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@answers_bp.route('/<int:answer_id>/vote', methods=['POST'])
@login_required
def vote_answer(answer_id):
    """Vote on an answer (upvote or downvote)"""
    from app.models import Vote
    
    answer = Answer.query.get_or_404(answer_id)
    data = request.get_json()
    
    if 'vote_type' not in data or data['vote_type'] not in ['up', 'down']:
        return jsonify({"error": "Invalid vote type. Must be 'up' or 'down'"}), 400
    
    vote_type = data['vote_type']
    
    try:
        # Check if user already voted on this answer
        existing_vote = Vote.query.filter_by(
            answer_id=answer_id,
            user_id=g.user.id
        ).first()
        
        if existing_vote:
            if existing_vote.vote_type == vote_type:
                # If voting the same way, remove the vote
                db.session.delete(existing_vote)
            else:
                # If voting differently, update the vote
                existing_vote.vote_type = vote_type
        else:
            # Create new vote
            vote = Vote(
                answer_id=answer_id,
                user_id=g.user.id,
                vote_type=vote_type
            )
            db.session.add(vote)
        
        db.session.commit()
        
        # Return updated answer with vote counts
        return jsonify(answer.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500