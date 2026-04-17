import unittest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_analyze_personality(self):
        sample_answers = [4, 5, 3, 4, 5, 4, 4, 3, 5, 4,
                         5, 4, 4, 5, 5, 4, 4, 4, 3, 4,
                         3, 4, 5, 4, 3, 4, 3, 4, 4, 3,
                         5, 5, 4, 4, 5, 4, 5, 5, 4, 4,
                         3, 4, 3, 4, 3, 4, 3, 3, 4, 3]
        
        response = self.client.post('/api/personality/analyze',
                                    data=json.dumps({'answers': sample_answers}),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('traits', data)
        self.assertIn('personality_type', data)
    
    def test_analyze_personality_invalid_answers(self):
        response = self.client.post('/api/personality/analyze',
                                    data=json.dumps({'answers': [1, 2, 3]}),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_career_recommendations(self):
        traits = {
            'openness': 75,
            'conscientiousness': 80,
            'extraversion': 45,
            'agreeableness': 55,
            'neuroticism': 35
        }
        
        response = self.client.post('/api/recommendations/careers',
                                   data=json.dumps(traits),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('careers', data)
        self.assertIsInstance(data['careers'], list)
    
    def test_login_missing_fields(self):
        response = self.client.post('/api/auth/login',
                                    data=json.dumps({'email': 'test@example.com'}),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_register_missing_fields(self):
        response = self.client.post('/api/auth/register',
                                    data=json.dumps({'name': 'Test'}),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
