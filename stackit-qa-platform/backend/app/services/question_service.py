from app import db
from app.models import Question, Tag
from sqlalchemy import or_

class QuestionService:
    """
    Service class for handling question-related operations
    """
    
    @staticmethod
    def get_questions(page=1, per_page=10, tag=None, search=None):
        """
        Get questions with optional filtering by tag and search terms
        """
        query = Question.query
        
        # Filter by tag if provided
        if tag:
            query = query.join(Question.tags).filter(Tag.name == tag)
        
        # Filter by search terms if provided
        if search:
            search_terms = f"%{search}%"
            query = query.filter(
                or_(
                    Question.title.ilike(search_terms),
                    Question.description.ilike(search_terms)
                )
            )
        
        # Order by most recent
        query = query.order_by(Question.created_at.desc())
        
        # Paginate results
        questions_page = query.paginate(page=page, per_page=per_page)
        
        return {
            'questions': [q.to_dict() for q in questions_page.items],
            'total': questions_page.total,
            'page': page,
            'per_page': per_page,
            'pages': questions_page.pages
        }

    @staticmethod
    def get_question_by_id(question_id):
        """
        Get a specific question by its ID
        """
        return Question.query.get(question_id)

    @staticmethod
    def create_question(user_id, title, description, tags=None):
        """
        Create a new question with optional tags
        """
        # Create new question
        question = Question(
            user_id=user_id,
            title=title,
            description=description
        )
        db.session.add(question)
        
        # Add tags if provided
        if tags:
            for tag_name in tags:
                # Get or create tag
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                question.tags.append(tag)
        
        db.session.commit()
        return question