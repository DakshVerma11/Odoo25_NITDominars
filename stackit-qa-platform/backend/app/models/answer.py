from datetime import datetime
from app import db

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    accepted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    votes = db.relationship('Vote', backref='answer', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='answer', lazy=True, cascade="all, delete-orphan")
    
    def to_dict(self, include_votes=True, include_comments=False):
        data = {
            'id': self.id,
            'question_id': self.question_id,
            'user_id': self.user_id,
            'author': self.author.username,
            'content': self.content,
            'accepted': self.accepted,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_votes:
            upvotes = sum(1 for vote in self.votes if vote.vote_type == 'up')
            downvotes = sum(1 for vote in self.votes if vote.vote_type == 'down')
            data['score'] = upvotes - downvotes
            data['upvotes'] = upvotes
            data['downvotes'] = downvotes
            
        if include_comments:
            data['comments'] = [comment.to_dict() for comment in self.comments]
            
        return data