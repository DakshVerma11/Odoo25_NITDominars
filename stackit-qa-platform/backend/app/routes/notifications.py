from flask import Blueprint, jsonify, g, Response, request, abort
import json
import queue
import threading
import time
from app import db
from app.models import Notification
from app.utils.decorators import login_required
from app.services.notification_service import get_user_notifications, mark_notification_as_read

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

# In-memory event sources for SSE
event_sources = {}

@notifications_bp.route('', methods=['GET'])
@login_required
def get_notifications():
    """Get all notifications for the current user"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    unread_only = request.args.get('unread', 'false').lower() == 'true'
    
    notifications, total = get_user_notifications(g.user.id, page, per_page, unread_only)
    
    return jsonify({
        'notifications': [n.to_dict() for n in notifications],
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    })

@notifications_bp.route('/<int:notification_id>/read', methods=['PUT'])
@login_required
def mark_read(notification_id):
    """Mark a notification as read"""
    notification = Notification.query.get_or_404(notification_id)
    
    # Ensure notification belongs to current user
    if notification.user_id != g.user.id:
        abort(403, description="Permission denied")
    
    mark_notification_as_read(notification_id)
    
    return jsonify({"message": "Notification marked as read"})

@notifications_bp.route('/read-all', methods=['PUT'])
@login_required
def mark_all_read():
    """Mark all user notifications as read"""
    try:
        Notification.query.filter_by(user_id=g.user.id, read=False).update({"read": True})
        db.session.commit()
        return jsonify({"message": "All notifications marked as read"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@notifications_bp.route('/stream')
@login_required
def notification_stream():
    """SSE endpoint for real-time notifications"""
    def generate():
        # Create a queue for this user if it doesn't exist
        if g.user.id not in event_sources:
            event_sources[g.user.id] = queue.Queue()
        
        user_queue = event_sources[g.user.id]
        
        # Send headers for SSE
        yield "event: connected\ndata: {\"status\": \"connected\"}\n\n"
        
        try:
            while True:
                try:
                    # Non-blocking queue get with timeout
                    message = user_queue.get(timeout=30)
                    yield f"data: {json.dumps(message)}\n\n"
                except queue.Empty:
                    # Send a heartbeat to keep connection alive
                    yield "event: ping\ndata: {}\n\n"
                    
                time.sleep(0.1)  # Small delay to prevent CPU overuse
        finally:
            # Clean up when client disconnects
            if g.user.id in event_sources:
                del event_sources[g.user.id]
    
    return Response(generate(), mimetype='text/event-stream')