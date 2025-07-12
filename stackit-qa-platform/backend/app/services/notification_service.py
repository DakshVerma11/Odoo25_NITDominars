from app import db
from app.models import Notification, User
from flask import current_app

def get_user_notifications(user_id, page=1, per_page=10, unread_only=False):
    """
    Get notifications for a specific user with pagination
    """
    query = Notification.query.filter_by(user_id=user_id)
    
    if unread_only:
        query = query.filter_by(read=False)
    
    # Order by most recent
    query = query.order_by(Notification.created_at.desc())
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    notifications = query.paginate(page=page, per_page=per_page).items
    
    return notifications, total

def create_notification(user_id, notification_type, source_id):
    """
    Create a new notification and push to real-time stream if available
    """
    try:
        # Create notification in database
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            source_id=source_id
        )
        db.session.add(notification)
        db.session.commit()
        
        # Send to real-time stream if user is connected
        push_notification_to_stream(notification)
        
        return notification
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating notification: {str(e)}")
        return None

def mark_notification_as_read(notification_id):
    """
    Mark a notification as read
    """
    try:
        notification = Notification.query.get(notification_id)
        if notification:
            notification.read = True
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error marking notification as read: {str(e)}")
        return False

def push_notification_to_stream(notification):
    """
    Push a notification to the user's SSE stream if they're connected
    """
    from app.routes.notifications import event_sources
    
    user_id = notification.user_id
    if user_id in event_sources:
        try:
            # Add the notification to the user's queue (non-async approach)
            event_sources[user_id].put(notification.to_dict())
        except Exception as e:
            current_app.logger.error(f"Error pushing to notification stream: {str(e)}")