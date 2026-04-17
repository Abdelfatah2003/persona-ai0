"""
Comprehensive Test Suite for AI Personality & Career Recommendation System
"""
import unittest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from ai_engine.personality_analyzer import PersonalityAnalyzer
from ai_engine.text_processor import TextProcessor
from ai_engine.ml_predictor import PersonalityPredictor
from ai_engine.recommender.career_recommender import CareerRecommender
from ai_engine.recommender.user_recommender import UserRecommender
from ai_engine.recommender.similarity import cosine_similarity, euclidean_distance
from backend.security import InputValidator, SecurityManager


class TestPersonalityAnalyzer(unittest.TestCase):
    """Test cases for PersonalityAnalyzer"""
    
    def setUp(self):
        self.analyzer = PersonalityAnalyzer()
        self.sample_answers = [4, 4, 5, 4, 5, 4, 3, 5, 4, 5,  # Openness
                              5, 4, 4, 5, 4, 5, 4, 4, 5, 4,  # Conscientiousness
                              3, 3, 4, 3, 4, 3, 3, 4, 3, 3,  # Extraversion
                              5, 5, 4, 5, 5, 4, 5, 5, 4, 5,  # Agreeableness
                              2, 3, 2, 3, 2, 3, 2, 2, 3, 2]  # Neuroticism
    
    def test_calculate_traits_returns_dict(self):
        """Test that calculate_traits returns a dictionary"""
        result = self.analyzer.calculate_traits(self.sample_answers)
        self.assertIsInstance(result, dict)
    
    def test_calculate_traits_has_five_traits(self):
        """Test that exactly five traits are returned"""
        result = self.analyzer.calculate_traits(self.sample_answers)
        self.assertEqual(len(result), 5)
        self.assertIn('openness', result)
        self.assertIn('conscientiousness', result)
        self.assertIn('extraversion', result)
        self.assertIn('agreeableness', result)
        self.assertIn('neuroticism', result)
    
    def test_traits_are_within_range(self):
        """Test that all trait values are between 0 and 100"""
        result = self.analyzer.calculate_traits(self.sample_answers)
        for trait, value in result.items():
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 100)
    
    def test_invalid_answer_count(self):
        """Test that invalid answer count raises error"""
        with self.assertRaises(ValueError):
            self.analyzer.calculate_traits([1, 2, 3])
    
    def test_analyze_text_returns_dict(self):
        """Test that analyze_text returns personality traits"""
        text = "I enjoy solving technical problems and working alone on the computer"
        result = self.analyzer.analyze_text(text)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 5)
    
    def test_get_personality_type_returns_string(self):
        """Test that personality type is a string"""
        traits = {'openness': 75, 'conscientiousness': 65, 'extraversion': 45, 
                  'agreeableness': 55, 'neuroticism': 35}
        result = self.analyzer.get_personality_type(traits)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)


class TestTextProcessor(unittest.TestCase):
    """Test cases for TextProcessor"""
    
    def setUp(self):
        self.processor = TextProcessor()
    
    def test_preprocess_removes_urls(self):
        """Test that URLs are removed"""
        text = "Check this https://example.com and this http://test.com"
        result = self.processor.preprocess(text)
        self.assertNotIn('http', result)
        self.assertNotIn('example.com', result)
    
    def test_preprocess_removes_mentions(self):
        """Test that @mentions are removed"""
        text = "Hello @username and @another_user"
        result = self.processor.preprocess(text)
        self.assertNotIn('@username', result)
    
    def test_preprocess_removes_hashtags(self):
        """Test that #hashtags are removed"""
        text = "Testing #python and #coding"
        result = self.processor.preprocess(text)
        self.assertNotIn('#', result)
    
    def test_preprocess_removes_numbers(self):
        """Test that numbers are removed"""
        text = "I have 5 cats and 3 dogs"
        result = self.processor.preprocess(text)
        self.assertNotIn('5', result)
        self.assertNotIn('3', result)
    
    def test_extract_keywords_returns_list(self):
        """Test that keywords extraction returns a list"""
        text = "creative artistic curious imaginative artistic creative curious"
        result = self.processor.extract_keywords(text)
        self.assertIsInstance(result, list)
    
    def test_extract_keywords_respects_top_n(self):
        """Test that top_n parameter is respected"""
        text = "one two three four five six seven eight nine ten"
        result = self.processor.extract_keywords(text, top_n=5)
        self.assertEqual(len(result), 5)
    
    def test_tokenize_returns_list(self):
        """Test that tokenization returns a list"""
        text = "Hello world test"
        result = self.processor.tokenize(text)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
    
    def test_to_vector(self):
        """Test text to vector conversion"""
        text = "hello world"
        vocabulary = ['hello', 'world', 'test']
        result = self.processor.to_vector(text, vocabulary)
        self.assertEqual(result, [1, 1, 0])


class TestMLPredictor(unittest.TestCase):
    """Test cases for ML-based Personality Predictor"""
    
    def setUp(self):
        self.predictor = PersonalityPredictor()
    
    def test_analyze_text_advanced(self):
        """Test advanced text analysis"""
        text = "I am creative and curious. I enjoy art and exploring new ideas."
        result = self.predictor.analyze_text_advanced(text)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 5)
        self.assertGreater(result['openness'], 50)
    
    def test_calculate_traits_from_answers(self):
        """Test trait calculation from quiz answers"""
        answers = [5]*10 + [5]*10 + [3]*10 + [5]*10 + [2]*10
        result = self.predictor.calculate_traits_from_answers(answers)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 5)
    
    def test_predict_personality_type(self):
        """Test personality type prediction"""
        traits = {'openness': 80, 'conscientiousness': 70, 'extraversion': 45,
                  'agreeableness': 55, 'neuroticism': 30}
        result = self.predictor.predict_personality_type(traits)
        self.assertIsInstance(result, list)
        self.assertIn('Explorer', result)
    
    def test_recommend_careers(self):
        """Test career recommendation"""
        traits = {'openness': 75, 'conscientiousness': 70, 'extraversion': 40,
                  'agreeableness': 55, 'neuroticism': 45}
        result = self.predictor.recommend_careers(traits, top_n=3)
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 3)
        self.assertGreater(result[0]['match_score'], 0)
    
    def test_analyze_combined_with_answers(self):
        """Test combined analysis with quiz answers"""
        answers = [4]*50
        result = self.predictor.analyze_combined(answers=answers)
        self.assertIn('traits', result)
        self.assertIn('personality_types', result)
        self.assertIn('career_recommendations', result)
    
    def test_get_personality_description(self):
        """Test personality description generation"""
        types = ['Explorer', 'Achiever']
        result = self.predictor.get_personality_description(types)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)


class TestCareerRecommender(unittest.TestCase):
    """Test cases for CareerRecommender"""
    
    def setUp(self):
        self.recommender = CareerRecommender()
    
    def test_calculate_match_score(self):
        """Test match score calculation"""
        user_traits = {'openness': 70, 'conscientiousness': 75, 'extraversion': 40}
        career_traits = {'openness': 65, 'conscientiousness': 70, 'extraversion': 45}
        result = self.recommender.calculate_match_score(user_traits, career_traits)
        self.assertGreater(result, 0)
        self.assertLessEqual(result, 100)
    
    def test_get_recommendations(self):
        """Test that recommendations are returned"""
        traits = {'openness': 75, 'conscientiousness': 70, 'extraversion': 40,
                  'agreeableness': 55, 'neuroticism': 45}
        result = self.recommender.get_recommendations(traits)
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 5)
    
    def test_get_skills_for_career(self):
        """Test skills retrieval for career"""
        result = self.recommender.get_skills_for_career('Software Engineer')
        self.assertIsInstance(result, list)
        self.assertIn('Python', result)


class TestSimilarityFunctions(unittest.TestCase):
    """Test cases for similarity functions"""
    
    def test_cosine_similarity_identical(self):
        """Test cosine similarity of identical vectors"""
        vec = [1, 2, 3, 4, 5]
        result = cosine_similarity(vec, vec)
        self.assertAlmostEqual(result, 1.0, places=5)
    
    def test_cosine_similarity_opposite(self):
        """Test cosine similarity of opposite vectors"""
        vec1 = [1, 2, 3, 4, 5]
        vec2 = [-1, -2, -3, -4, -5]
        result = cosine_similarity(vec1, vec2)
        self.assertAlmostEqual(result, -1.0, places=5)
    
    def test_cosine_similarity_zero(self):
        """Test cosine similarity with zero vectors"""
        result = cosine_similarity([0, 0, 0], [1, 2, 3])
        self.assertEqual(result, 0.0)
    
    def test_euclidean_distance(self):
        """Test euclidean distance"""
        result = euclidean_distance([0, 0], [3, 4])
        self.assertAlmostEqual(result, 5.0, places=5)
    
    def test_euclidean_distance_zero(self):
        """Test euclidean distance of identical points"""
        result = euclidean_distance([1, 2, 3], [1, 2, 3])
        self.assertEqual(result, 0.0)


class TestInputValidator(unittest.TestCase):
    """Test cases for InputValidator"""
    
    def test_validate_email_valid(self):
        """Test valid email validation"""
        valid, error = InputValidator.validate_email("test@example.com")
        self.assertTrue(valid)
        self.assertIsNone(error)
    
    def test_validate_email_invalid_no_at(self):
        """Test invalid email without @"""
        valid, error = InputValidator.validate_email("testexample.com")
        self.assertFalse(valid)
        self.assertIsNotNone(error)
    
    def test_validate_email_invalid_no_domain(self):
        """Test invalid email without domain"""
        valid, error = InputValidator.validate_email("test@")
        self.assertFalse(valid)
    
    def test_validate_password_valid(self):
        """Test valid password"""
        valid, error = InputValidator.validate_password("Password123")
        self.assertTrue(valid)
        self.assertIsNone(error)
    
    def test_validate_password_too_short(self):
        """Test password too short"""
        valid, error = InputValidator.validate_password("Pass1")
        self.assertFalse(valid)
    
    def test_validate_password_no_uppercase(self):
        """Test password without uppercase"""
        valid, error = InputValidator.validate_password("password123")
        self.assertFalse(valid)
    
    def test_validate_name_valid(self):
        """Test valid name"""
        valid, error = InputValidator.validate_name("John Doe")
        self.assertTrue(valid)
    
    def test_validate_name_invalid_characters(self):
        """Test name with invalid characters"""
        valid, error = InputValidator.validate_name("John123")
        self.assertFalse(valid)
    
    def test_validate_age_valid(self):
        """Test valid age"""
        valid, error = InputValidator.validate_age(25)
        self.assertTrue(valid)
    
    def test_validate_age_too_young(self):
        """Test age too young"""
        valid, error = InputValidator.validate_age(5)
        self.assertFalse(valid)
    
    def test_validate_quiz_answers_valid(self):
        """Test valid quiz answers"""
        answers = [1, 2, 3, 4, 5] * 10
        valid, error = InputValidator.validate_quiz_answers(answers)
        self.assertTrue(valid)
    
    def test_validate_quiz_answers_invalid_count(self):
        """Test quiz answers with wrong count"""
        answers = [1, 2, 3]
        valid, error = InputValidator.validate_quiz_answers(answers)
        self.assertFalse(valid)
    
    def test_sanitize_input_removes_html(self):
        """Test HTML tag removal"""
        result = InputValidator.sanitize_input("<script>alert('xss')</script>Hello")
        self.assertNotIn("<script>", result)
        self.assertIn("Hello", result)


class TestAPIRoutes(unittest.TestCase):
    """Test cases for API routes"""
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        self.client = app.test_client()
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_register_missing_fields(self):
        """Test registration with missing fields"""
        response = self.client.post('/api/auth/register',
                                     json={'name': 'Test'},
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_register_valid(self):
        """Test valid registration"""
        response = self.client.post('/api/auth/register',
                                     json={
                                         'name': 'Test User',
                                         'email': 'test@example.com',
                                         'password': 'Password123'
                                     },
                                     content_type='application/json')
        self.assertIn(response.status_code, [201, 409])  # 409 if user exists
    
    def test_login_missing_fields(self):
        """Test login with missing fields"""
        response = self.client.post('/api/auth/login',
                                     json={'email': 'test@example.com'},
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_personality_analyze_missing_answers(self):
        """Test personality analysis without answers"""
        response = self.client.post('/api/personality/analyze',
                                     json={},
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_personality_analyze_invalid_count(self):
        """Test personality analysis with wrong answer count"""
        response = self.client.post('/api/personality/analyze',
                                     json={'answers': [1, 2, 3]},
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_full_user_flow(self):
        """Test complete user journey"""
        # 1. Register
        register_response = self.client.post('/api/auth/register',
                                              json={
                                                  'name': 'Integration Test',
                                                  'email': 'integration@example.com',
                                                  'password': 'TestPass123'
                                              },
                                              content_type='application/json')
        
        # 2. Login
        login_response = self.client.post('/api/auth/login',
                                          json={
                                              'email': 'integration@example.com',
                                              'password': 'TestPass123'
                                          },
                                          content_type='application/json')
        
        # 3. Take personality quiz
        answers = [4]*10 + [4]*10 + [3]*10 + [4]*10 + [2]*10
        quiz_response = self.client.post('/api/personality/save',
                                         json={
                                             'email': 'integration@example.com',
                                             'answers': answers,
                                             'traits': {
                                                 'openness': 80,
                                                 'conscientiousness': 80,
                                                 'extraversion': 60,
                                                 'agreeableness': 80,
                                                 'neuroticism': 40
                                             }
                                         },
                                         content_type='application/json')
        
        # 4. Get career recommendations
        career_response = self.client.post('/api/recommendations/careers',
                                            json={
                                                'openness': 80,
                                                'conscientiousness': 80,
                                                'extraversion': 60,
                                                'agreeableness': 80,
                                                'neuroticism': 40
                                            },
                                            content_type='application/json')
        
        if career_response.status_code == 200:
            data = json.loads(career_response.data)
            self.assertIn('careers', data)


if __name__ == '__main__':
    unittest.main()
