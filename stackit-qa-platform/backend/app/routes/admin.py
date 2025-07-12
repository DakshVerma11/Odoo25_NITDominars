from flask import Blueprint, request, jsonify, g, abort
from app import db
from app.models import User, Question, Answer, Tag
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users (admin only)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    
    if search:
        query = query.filter(User.username.ilike(f'%{search}%') | User.email.ilike(f'%{search}%'))
    
    users_page = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        "users": [u.to_dict(include_email=True) for u in users_page.items],
        "total": users_page.total,
        "page": page,
        "pages": users_page.pages,
        "per_page": per_page
    })

@admin_bp.route('/users/<int:user_id>/ban', methods=['PUT'])
@admin_required
def ban_user(user_id):
    """Ban or unban a user (admin only)"""
    user = User.query.get_or_404(user_id)
    
    # Admin can't ban themselves
    if user.id == g.user.id:
        return jsonify({"error": "You cannot ban yourself"}), 400
    
    # Can't ban other admins
    if user.is_admin():
        return jsonify({"error": "Cannot ban an admin user"}), 400
    
    data = request.get_json()
    ban_status = data.get('banned', True)
    
    user.banned = ban_status
    
    try:
        db.session.commit()
        action = "banned" if ban_status else "unbanned"
        return jsonify({"message": f"User {action} successfully", "user": user.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_platform_stats():
    """Get platform statistics (admin only)"""
    total_users = User.query.count()
    total_questions = Question.query.count()
    total_answers = Answer.query.count()
    total_tags = Tag.query.count()
    
    # Get recently joined users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # Get recently asked questions
    recent_questions = Question.query.order_by(Question.created_at.desc()).limit(5).all()
    
    # Get tags with most questions
    popular_tags_query = db.session.query(
        Tag, db.func.count(question_tags.c.question_id).label('question_count')
    ).join(
        question_tags, Tag.id == question_tags.c.tag_id
    ).group_by(
        Tag.id
    ).order_by(
        db.desc('question_count')
    ).limit(10)
    
    popular_tags = [{"name": tag.name, "count": count} for tag, count in popular_tags_query]
    
    return jsonify({
        "stats": {
            "users": total_users,
            "questions": total_questions,
            "answers": total_answers,
            "tags": total_tags,
            "answer_ratio": round(total_answers / total_questions, 2) if total_questions > 0 else 0
        },
        "recent_users": [u.to_dict() for u in recent_users],
        "recent_questions": [q.to_dict() for q in recent_questions],
        "popular_tags": popular_tags
    })

@admin_bp.route('/questions/<int:question_id>', methods=['DELETE'])
@admin_required
def delete_question(question_id):
    """Delete a question (admin only)"""
    question = Question.query.get_or_404(question_id)
    
    try:
        db.session.delete(question)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/answers/<int:answer_id>', methods=['DELETE'])
@admin_required
def delete_answer(answer_id):
    """Delete an answer (admin only)"""
    answer = Answer.query.get_or_404(answer_id)
    
    try:
        db.session.delete(answer)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500