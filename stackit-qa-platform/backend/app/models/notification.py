from datetime import datetime
from app import db

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    type = db.Column(db.Enum('answer', 'comment', 'mention', name='notification_types'), nullable=False)
    source_id = db.Column(db.Integer, nullable=False)  # ID of answer/comment that triggered notification
    read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'source_id': self.source_id,
            'read': self.read,
            'created_at': self.created_at.isoformat()
        }