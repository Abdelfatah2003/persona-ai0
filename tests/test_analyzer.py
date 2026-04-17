import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_engine.personality_analyzer import PersonalityAnalyzer

class TestPersonalityAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PersonalityAnalyzer()
        self.sample_answers = [4, 5, 3, 4, 5, 4, 4, 3, 5, 4,
                              5, 4, 4, 5, 5, 4, 4, 4, 3, 4,
                              3, 4, 5, 4, 3, 4, 3, 4, 4, 3,
                              5, 5, 4, 4, 5, 4, 5, 5, 4, 4,
                              3, 4, 3, 4, 3, 4, 3, 3, 4, 3]
    
    def test_calculate_traits(self):
        traits = self.analyzer.calculate_traits(self.sample_answers)
        
        self.assertIn('openness', traits)
        self.assertIn('conscientiousness', traits)
        self.assertIn('extraversion', traits)
        self.assertIn('agreeableness', traits)
        self.assertIn('neuroticism', traits)
        
        for trait_value in traits.values():
            self.assertGreaterEqual(trait_value, 0)
            self.assertLessEqual(trait_value, 100)
    
    def test_invalid_answers_length(self):
        with self.assertRaises(ValueError):
            self.analyzer.calculate_traits([1, 2, 3])
    
    def test_get_personality_type(self):
        traits = {
            'openness': 75,
            'conscientiousness': 80,
            'extraversion': 30,
            'agreeableness': 50,
            'neuroticism': 40
        }
        
        personality_type = self.analyzer.get_personality_type(traits)
        self.assertIn('Explorer', personality_type)
        self.assertIn('Achiever', personality_type)
    
    def test_compare_traits(self):
        traits1 = {'openness': 70, 'conscientiousness': 80, 'extraversion': 50, 'agreeableness': 60, 'neuroticism': 40}
        traits2 = {'openness': 75, 'conscientiousness': 85, 'extraversion': 55, 'agreeableness': 65, 'neuroticism': 45}
        
        difference = self.analyzer.compare_traits(traits1, traits2)
        self.assertLessEqual(difference, 10)

if __name__ == '__main__':
    unittest.main()
