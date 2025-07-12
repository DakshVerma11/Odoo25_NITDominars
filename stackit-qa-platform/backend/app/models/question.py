from datetime import datetime
from app import db

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    answers = db.relationship('Answer', backref='question', lazy=True, cascade="all, delete-orphan")
    tags = db.relationship('Tag', secondary='question_tags', backref=db.backref('questions', lazy=True))
    
    def to_dict(self, include_answers=False, include_tags=True):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'author': self.author.username,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_tags:
            data['tags'] = [tag.name for tag in self.tags]
            
        if include_answers:
            data['answers'] = [answer.to_dict() for answer in self.answers]
            data['answer_count'] = len(self.answers)
            
        return data