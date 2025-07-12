from app import db
from app.models import Answer, Vote, Comment
from app.utils.helpers import sanitize_html
from app.services.notification_service import create_notification
import re

def get_answer_by_id(answer_id):
    """
    Get a specific answer by ID
    """
    return Answer.query.get(answer_id)

def create_answer(user_id, question_id, content):
    """
    Create a new answer to a question and send notifications
    """
    # Sanitize content
    clean_content = sanitize_html(content)
    
    # Create answer
    answer = Answer(
        user_id=user_id,
        question_id=question_id,
        content=clean_content
    )
    
    db.session.add(answer)
    db.session.commit()
    
    # Get question author for notification
    from app.models import Question
    question = Question.query.get(question_id)
    
    # Notify question author if different from answer author
    if question.user_id != user_id:
        create_notification(
            user_id=question.user_id,
            notification_type='answer',
            source_id=answer.id
        )
    
    # Process mentions to notify users
    process_mentions(clean_content, answer.id)
    
    return answer

def update_answer(answer_id, content):
    """
    Update an existing answer
    """
    answer = Answer.query.get(answer_id)
    if not answer:
        return None
    
    # Sanitize content
    clean_content = sanitize_html(content)
    
    # Update answer
    answer.content = clean_content
    db.session.commit()
    
    return answer

def process_mentions(content, answer_id):
    """
    Extract @username mentions from content and create notifications
    """
    # Find all @username patterns in the content
    pattern = r'@([a-zA-Z0-9_]{3,})'
    mentions = re.findall(pattern, content)
    
    if not mentions:
        return
    
    # Get the answer to determine who wrote it
    answer = Answer.query.get(answer_id)
    if not answer:
        return
    
    # Get mentioned users and send notifications
    from app.models import User
    for username in set(mentions):
        mentioned_user = User.query.filter_by(username=username).first()
        
        # Only notify if user exists and is not the answer author
        if mentioned_user and mentioned_user.id != answer.user_id:
            create_notification(
                user_id=mentioned_user.id,
                notification_type='mention',
                source_id=answer_id
            )

def create_comment(user_id, answer_id, content):
    """
    Create a comment on an answer and notify the answer author
    """
    # Create comment
    comment = Comment(
        user_id=user_id,
        answer_id=answer_id,
        content=content
    )
    
    db.session.add(comment)
    db.session.commit()
    
    # Get answer author for notification
    answer = Answer.query.get(answer_id)
    
    # Notify answer author if different from commenter
    if answer.user_id != user_id:
        create_notification(
            user_id=answer.user_id,
            notification_type='comment',
            source_id=comment.id
        )
    
    return comment

def vote_on_answer(user_id, answer_id, vote_type):
    """
    Register a vote (up/down) on an answer
    """
    # Check if user already voted
    existing_vote = Vote.query.filter_by(
        user_id=user_id,
        answer_id=answer_id
    ).first()
    
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Remove vote if same type (toggle off)
            db.session.delete(existing_vote)
        else:
            # Change vote type
            existing_vote.vote_type = vote_type
    else:
        # Create new vote
        vote = Vote(
            user_id=user_id,
            answer_id=answer_id,
            vote_type=vote_type
        )
        db.session.add(vote)
    
    db.session.commit()
    
    # Return updated vote counts
    return get_vote_counts(answer_id)

def get_vote_counts(answer_id):
    """
    Get upvote and downvote counts for an answer
    """
    upvotes = Vote.query.filter_by(answer_id=answer_id, vote_type='up').count()
    downvotes = Vote.query.filter_by(answer_id=answer_id, vote_type='down').count()
    
    return {
        'upvotes': upvotes,
        'downvotes': downvotes,
        'score': upvotes - downvotes
    }