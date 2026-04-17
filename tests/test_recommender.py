import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_engine.recommender.career_recommender import CareerRecommender
from ai_engine.recommender.similarity import cosine_similarity, euclidean_distance

class TestCareerRecommender(unittest.TestCase):
    def setUp(self):
        self.recommender = CareerRecommender()
        self.sample_traits = {
            'openness': 75,
            'conscientiousness': 80,
            'extraversion': 45,
            'agreeableness': 55,
            'neuroticism': 35
        }
    
    def test_get_recommendations(self):
        recommendations = self.recommender.get_recommendations(self.sample_traits)
        
        self.assertIsInstance(recommendations, list)
        self.assertLessEqual(len(recommendations), 5)
        
        for rec in recommendations:
            self.assertIn('name', rec)
            self.assertIn('match_score', rec)
            self.assertIn('skills', rec)
            self.assertGreaterEqual(rec['match_score'], 0)
    
    def test_calculate_match_score(self):
        career_traits = {'openness': 70, 'conscientiousness': 75}
        score = self.recommender.calculate_match_score(self.sample_traits, career_traits)
        
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_get_skills_for_career(self):
        skills = self.recommender.get_skills_for_career('Software Engineer')
        self.assertIn('Python', skills)
        self.assertIn('JavaScript', skills)

class TestSimilarity(unittest.TestCase):
    def test_cosine_similarity_identical(self):
        vec = [1, 2, 3, 4, 5]
        sim = cosine_similarity(vec, vec)
        self.assertAlmostEqual(sim, 1.0)
    
    def test_cosine_similarity_opposite(self):
        vec1 = [1, 2, 3]
        vec2 = [-1, -2, -3]
        sim = cosine_similarity(vec1, vec2)
        self.assertAlmostEqual(sim, -1.0)
    
    def test_cosine_similarity_zero_vector(self):
        vec1 = [0, 0, 0]
        vec2 = [1, 2, 3]
        sim = cosine_similarity(vec1, vec2)
        self.assertEqual(sim, 0.0)
    
    def test_euclidean_distance(self):
        vec1 = [0, 0]
        vec2 = [3, 4]
        dist = euclidean_distance(vec1, vec2)
        self.assertAlmostEqual(dist, 5.0)

if __name__ == '__main__':
    unittest.main()
