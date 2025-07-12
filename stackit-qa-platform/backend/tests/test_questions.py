import unittest
import json
from app import create_app, db
from app.models import User, Question, Tag

class QuestionsTestCase(unittest.TestCase):
    """Test case for questions endpoints"""
    
    def setUp(self):
        """Set up test client and database"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user
        self.user = User(
            username='testuser',
            email='test@example.com'
        )
        self.user.set_password('Password123')
        db.session.add(self.user)
        
        # Create test tag
        self.tag = Tag(name='test-tag')
        db.session.add(self.tag)
        
        # Create test question
        self.question = Question(
            user_id=1,
            title='Test Question Title',
            description='This is a test question description with enough characters.'
        )
        self.question.tags.append(self.tag)
        db.session.add(self.question)
        
        db.session.commit()
        
        # Get auth token
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'Password123'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.auth_token = data['token']
    
    def tearDown(self):
        """Clean up after test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_get_questions(self):
        """Test getting all questions"""
        response = self.client.get('/api/questions')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('questions', data)
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['questions'][0]['title'], 'Test Question Title')
    
    def test_get_question(self):
        """Test getting a specific question"""
        response = self.client.get(f'/api/questions/{self.question.id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], 'Test Question Title')
        self.assertEqual(data['author'], 'testuser')
        self.assertIn('tags', data)
        self.assertEqual(data['tags'][0], 'test-tag')
    
    def test_create_question(self):
        """Test creating a new question"""
        response = self.client.post(
            '/api/questions',
            data=json.dumps({
                'title': 'New Question Title',
                'description': 'This is a new question description with enough characters.',
                'tags': ['python', 'flask']
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['title'], 'New Question Title')
        self.assertEqual(data['author'], 'testuser')
        self.assertIn('python', data['tags'])
        self.assertIn('flask', data['tags'])
        
        # Verify tags were created in database
        python_tag = Tag.query.filter_by(name='python').first()
        self.assertIsNotNone(python_tag)
    
    def test_update_question(self):
        """Test updating a question"""
        response = self.client.put(
            f'/api/questions/{self.question.id}',
            data=json.dumps({
                'title': 'Updated Question Title',
                'description': 'This is an updated question description with enough characters.',
                'tags': ['updated-tag']
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], 'Updated Question Title')
        self.assertIn('updated-tag', data['tags'])
        
        # Verify tags were updated in database
        updated_question = Question.query.get(self.question.id)
        self.assertEqual(len(updated_question.tags), 1)
        self.assertEqual(updated_question.tags[0].name, 'updated-tag')
    
    def test_delete_question(self):
        """Test deleting a question"""
        response = self.client.delete(
            f'/api/questions/{self.question.id}',
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        self.assertEqual(response.status_code, 204)
        
        # Verify question was deleted from database
        deleted_question = Question.query.get(self.question.id)
        self.assertIsNone(deleted_question)