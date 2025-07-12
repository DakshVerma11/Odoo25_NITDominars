import unittest
import json
from app import create_app, db
from app.models import User, Question, Answer, Vote

class AnswersTestCase(unittest.TestCase):
    """Test case for answers endpoints"""
    
    def setUp(self):
        """Set up test client and database"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test users
        self.user = User(
            username='testuser',
            email='test@example.com'
        )
        self.user.set_password('Password123')
        db.session.add(self.user)
        
        self.user2 = User(
            username='testuser2',
            email='test2@example.com'
        )
        self.user2.set_password('Password123')
        db.session.add(self.user2)
        
        # Create test question
        self.question = Question(
            user_id=1,
            title='Test Question Title',
            description='This is a test question description with enough characters.'
        )
        db.session.add(self.question)
        
        # Create test answer
        self.answer = Answer(
            question_id=1,
            user_id=2,  # Posted by user2
            content='This is a test answer with enough characters to be valid.'
        )
        db.session.add(self.answer)
        
        db.session.commit()
        
        # Get auth tokens
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
        
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'username': 'testuser2',
                'password': 'Password123'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.auth_token2 = data['token']
    
    def tearDown(self):
        """Clean up after test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_post_answer(self):
        """Test posting a new answer"""
        response = self.client.post(
            '/api/answers',
            data=json.dumps({
                'question_id': self.question.id,
                'content': 'This is a new answer with enough characters to be valid.'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['question_id'], self.question.id)
        self.assertEqual(data['author'], 'testuser')
        
        # Verify answer was created in database
        answer_count = Answer.query.filter_by(question_id=self.question.id).count()
        self.assertEqual(answer_count, 2)
    
    def test_update_answer(self):
        """Test updating an answer"""
        # User2 updating their own answer
        response = self.client.put(
            f'/api/answers/{self.answer.id}',
            data=json.dumps({
                'content': 'This is an updated answer with enough characters to be valid.'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.auth_token2}'}
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['content'], 'This is an updated answer with enough characters to be valid.')
        
        # User1 attempting to update User2's answer (should fail)
        response = self.client.put(
            f'/api/answers/{self.answer.id}',
            data=json.dumps({
                'content': 'This should not work because I am not the author.'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        self.assertEqual(response.status_code, 403)
    
    def test_accept_answer(self):
        """Test accepting an answer"""
        # User1 (question author) accepting User2's answer
        response = self.client.put(
            f'/api/answers/{self.answer.id}/accept',
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['accepted'])
        
        # User2 attempting to accept their own answer (should fail)
        response = self.client.put(
            f'/api/answers/{self.answer.id}/accept',
            headers={'Authorization': f'Bearer {self.auth_token2}'}
        )
        
        self.assertEqual(response.status_code, 403)
    
    def test_vote_answer(self):
        """Test voting on an answer"""
        # User1 upvoting User2's answer
        response = self.client.post(
            f'/api/answers/{self.answer.id}/vote',
            data=json.dumps({
                'vote_type': 'up'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['upvotes'], 1)
        self.assertEqual(data['downvotes'], 0)
        
        # User1 changing vote to downvote
        response = self.client.post(
            f'/api/answers/{self.answer.id}/vote',
            data=json.dumps({
                'vote_type': 'down'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['upvotes'], 0)
        self.assertEqual(data['downvotes'], 1)
        
        # User1 removing vote by voting the same way again
        response = self.client.post(
            f'/api/answers/{self.answer.id}/vote',
            data=json.dumps({
                'vote_type': 'down'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['upvotes'], 0)
        self.assertEqual(data['downvotes'], 0)