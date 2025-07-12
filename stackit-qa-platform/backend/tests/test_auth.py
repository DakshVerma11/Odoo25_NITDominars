import unittest
import json
from app import create_app, db
from app.models import User

class AuthTestCase(unittest.TestCase):
    """Test case for authentication endpoints"""
    
    def setUp(self):
        """Set up test client and database"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user
        test_user = User(
            username='testuser',
            email='test@example.com'
        )
        test_user.set_password('Password123')
        db.session.add(test_user)
        db.session.commit()
    
    def tearDown(self):
        """Clean up after test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_register_user(self):
        """Test user registration endpoint"""
        # Valid registration
        response = self.client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'newuser',
                'email': 'new@example.com',
                'password': 'Password123'
            }),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', data)
        self.assertEqual(data['user']['username'], 'newuser')
        
        # Test duplicate username
        response = self.client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'another@example.com',
                'password': 'Password123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 409)
        
        # Test invalid data
        response = self.client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'u',  # too short
                'email': 'invalid-email',
                'password': 'short'
            }),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', data)
        self.assertIn('username', data['errors'])
        self.assertIn('email', data['errors'])
        self.assertIn('password', data['errors'])
    
    def test_login(self):
        """Test user login endpoint"""
        # Valid login
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'Password123'
            }),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', data)
        self.assertEqual(data['user']['username'], 'testuser')
        
        # Invalid password
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'WrongPassword'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 401)
        
        # Non-existent user
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'username': 'nonexistentuser',
                'password': 'Password123'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 401)