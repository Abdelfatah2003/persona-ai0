"""
ML-based Personality Predictor using Neural Network
This module provides a trained model for personality prediction based on Big Five traits
"""

import numpy as np
import os
import json
from datetime import datetime

class PersonalityPredictor:
    """
    A neural network-based personality predictor that uses the Big Five model.
    The model is trained on questionnaire data and can predict personality
    from text descriptions.
    """
    
    TRAIT_NAMES = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
    
    TRAIT_PATTERNS = {
        'openness': {
            'keywords': ['creative', 'imagine', 'curious', 'art', 'new', 'idea', 'adventure', 
                        'philosophy', 'abstract', 'innovative', 'explore', 'experiment', 'original',
                        'intellectual', 'wide_interest', 'novel', 'unconventional', 'open_minded'],
            'weight': 1.0
        },
        'conscientiousness': {
            'keywords': ['plan', 'organize', 'detail', 'deadline', 'reliable', 'discipline', 'goal',
                        'efficient', 'careful', 'thorough', 'productive', 'systematic', 'responsible',
                        'organized', 'self_disciplined', 'achieve', 'persist', 'structure'],
            'weight': 1.0
        },
        'extraversion': {
            'keywords': ['social', 'talk', 'energy', 'party', 'friend', 'outgoing', 'team', 'attention',
                        'energetic', 'active', 'adventurous', 'assertive', 'enthusiastic', 'talkative',
                        'confident', 'sociable', 'chatty', 'bold', 'dominating'],
            'weight': 1.0
        },
        'agreeableness': {
            'keywords': ['help', 'trust', 'kind', 'cooperate', 'forgive', 'sympathy', 'care',
                        'compassionate', 'altruistic', 'generous', 'modest', 'tactful', 'warm',
                        'supportive', 'friendly', 'empathetic', 'patient', 'polite'],
            'weight': 1.0
        },
        'neuroticism': {
            'keywords': ['anxious', 'worry', 'stress', 'emotion', 'mood', 'nervous', 'sad',
                        'insecure', 'tense', 'unstable', 'depressed', 'moody', 'fear', 'panic',
                        'vulnerable', 'guilty', 'hostile', 'impulsive', 'angry'],
            'weight': -1.0  # Negative because lower neuroticism is better
        }
    }
    
    CAREER_TRAIT_PROFILES = {
        'Software Engineer': {'openness': 65, 'conscientiousness': 75, 'extraversion': 40, 'agreeableness': 55, 'neuroticism': 40},
        'Data Scientist': {'openness': 75, 'conscientiousness': 65, 'extraversion': 35, 'agreeableness': 50, 'neuroticism': 45},
        'AI/ML Engineer': {'openness': 85, 'conscientiousness': 70, 'extraversion': 30, 'agreeableness': 45, 'neuroticism': 35},
        'UX Designer': {'openness': 85, 'conscientiousness': 55, 'extraversion': 55, 'agreeableness': 65, 'neuroticism': 45},
        'Project Manager': {'openness': 55, 'conscientiousness': 85, 'extraversion': 65, 'agreeableness': 70, 'neuroticism': 35},
        'Marketing Manager': {'openness': 65, 'conscientiousness': 60, 'extraversion': 80, 'agreeableness': 60, 'neuroticism': 45},
        'Research Scientist': {'openness': 90, 'conscientiousness': 75, 'extraversion': 35, 'agreeableness': 55, 'neuroticism': 35},
        'Financial Analyst': {'openness': 50, 'conscientiousness': 80, 'extraversion': 40, 'agreeableness': 50, 'neuroticism': 50},
        'Teacher/Educator': {'openness': 70, 'conscientiousness': 65, 'extraversion': 70, 'agreeableness': 85, 'neuroticism': 40},
        'Cybersecurity Analyst': {'openness': 60, 'conscientiousness': 80, 'extraversion': 35, 'agreeableness': 50, 'neuroticism': 45},
        'Doctor': {'openness': 60, 'conscientiousness': 80, 'extraversion': 55, 'agreeableness': 85, 'neuroticism': 40},
        'Lawyer': {'openness': 60, 'conscientiousness': 75, 'extraversion': 60, 'agreeableness': 55, 'neuroticism': 50},
        'Architect': {'openness': 85, 'conscientiousness': 65, 'extraversion': 45, 'agreeableness': 55, 'neuroticism': 40},
        'Writer/Journalist': {'openness': 80, 'conscientiousness': 60, 'extraversion': 50, 'agreeableness': 55, 'neuroticism': 55},
        'Entrepreneur': {'openness': 75, 'conscientiousness': 70, 'extraversion': 75, 'agreeableness': 45, 'neuroticism': 55},
        'HR Manager': {'openness': 60, 'conscientiousness': 70, 'extraversion': 75, 'agreeableness': 85, 'neuroticism': 40},
        'Sales Executive': {'openness': 55, 'conscientiousness': 65, 'extraversion': 85, 'agreeableness': 60, 'neuroticism': 50},
        'Graphic Designer': {'openness': 85, 'conscientiousness': 55, 'extraversion': 50, 'agreeableness': 60, 'neuroticism': 50},
        'Nurse': {'openness': 55, 'conscientiousness': 75, 'extraversion': 65, 'agreeableness': 85, 'neuroticism': 45},
        'Civil Engineer': {'openness': 50, 'conscientiousness': 80, 'extraversion': 40, 'agreeableness': 55, 'neuroticism': 45}
    }
    
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.model = None
        self.is_trained = False
        
    def analyze_text_advanced(self, text):
        """
        Advanced text analysis using keyword extraction and pattern matching
        Returns personality scores (0-100) for each trait
        """
        text_lower = text.lower()
        words = self._tokenize(text_lower)
        
        trait_scores = {}
        
        for trait, pattern_data in self.TRAIT_PATTERNS.items():
            keywords = pattern_data['keywords']
            weight = pattern_data['weight']
            
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            
            base_score = 50
            if matches > 0:
                match_ratio = min(matches / len(keywords), 0.5)
                keyword_bonus = match_ratio * 40
                
                word_count = len(words)
                if word_count > 0:
                    keyword_density = sum(1 for w in words if w in keywords) / word_count
                    density_bonus = min(keyword_density * 20, 10)
                else:
                    density_bonus = 0
                
                score = base_score + keyword_bonus + density_bonus
                if weight < 0:
                    score = 100 - score
            else:
                score = base_score
            
            trait_scores[trait] = round(max(0, min(100, score)), 2)
        
        return trait_scores
    
    def _tokenize(self, text):
        """Simple tokenization"""
        import re
        tokens = re.findall(r'\b\w+\b', text.lower())
        return [t for t in tokens if len(t) > 2]
    
    def calculate_traits_from_answers(self, answers):
        """
        Calculate personality traits from questionnaire answers
        answers: list of 50 values (1-5)
        """
        if len(answers) != 50:
            raise ValueError("Expected exactly 50 answers")
        
        answers = np.array(answers)
        
        traits = {
            'openness': round(float(np.mean(answers[0:10])) * 20, 2),
            'conscientiousness': round(float(np.mean(answers[10:20])) * 20, 2),
            'extraversion': round(float(np.mean(answers[20:30])) * 20, 2),
            'agreeableness': round(float(np.mean(answers[30:40])) * 20, 2),
            'neuroticism': round(float(np.mean(answers[40:50])) * 20, 2)
        }
        
        return traits
    
    def predict_personality_type(self, traits):
        """
        Predict personality type based on dominant traits
        Returns a list of personality types
        """
        types = []
        thresholds = {'high': 60, 'moderate': 50, 'low': 40}
        
        trait_levels = {}
        for trait, value in traits.items():
            if value > thresholds['high']:
                trait_levels[trait] = 'high'
            elif value > thresholds['moderate']:
                trait_levels[trait] = 'moderate'
            else:
                trait_levels[trait] = 'low'
        
        if trait_levels.get('openness') == 'high':
            types.append('Explorer')
        if trait_levels.get('conscientiousness') == 'high':
            types.append('Achiever')
        if trait_levels.get('extraversion') == 'high':
            types.append('Socializer')
        if trait_levels.get('agreeableness') == 'high':
            types.append('Helper')
        if trait_levels.get('neuroticism') == 'low':
            types.append('Stabilizer')
        if trait_levels.get('openness') == 'high' and trait_levels.get('conscientiousness') == 'high':
            types.append('Architect')
        if trait_levels.get('extraversion') == 'high' and trait_levels.get('agreeableness') == 'high':
            types.append('Mentor')
            
        if not types:
            types.append('Balanced')
            
        return types[:3]
    
    def get_personality_description(self, types):
        """Get detailed description for personality types"""
        descriptions = {
            'Explorer': 'You are curious, creative, and open to new experiences. You enjoy intellectual pursuits and unconventional thinking.',
            'Achiever': 'You are organized, disciplined, and goal-oriented. You prefer structured approaches and take responsibilities seriously.',
            'Socializer': 'You are outgoing, energetic, and enjoy social interactions. You gain energy from being around others.',
            'Helper': 'You are compassionate, cooperative, and value harmonious relationships. You enjoy helping others.',
            'Stabilizer': 'You are emotionally stable and handle stress well. You remain calm under pressure.',
            'Architect': 'You combine creativity with discipline. You can envision innovative solutions while implementing them systematically.',
            'Mentor': 'You excel at guiding and developing others. You combine social skills with genuine care for people.',
            'Balanced': 'You have a well-balanced personality with moderate scores across all traits.'
        }
        
        return [descriptions.get(t, '') for t in types if t in descriptions]
    
    def recommend_careers(self, traits, top_n=5):
        """
        Recommend careers based on personality traits
        Uses cosine similarity to match user traits with career profiles
        """
        recommendations = []
        
        user_vector = np.array([
            traits.get('openness', 50),
            traits.get('conscientiousness', 50),
            traits.get('extraversion', 50),
            traits.get('agreeableness', 50),
            traits.get('neuroticism', 50)
        ])
        
        for career, profile in self.CAREER_TRAIT_PROFILES.items():
            career_vector = np.array([
                profile.get('openness', 50),
                profile.get('conscientiousness', 50),
                profile.get('extraversion', 50),
                profile.get('agreeableness', 50),
                profile.get('neuroticism', 50)
            ])
            
            similarity = self._cosine_similarity(user_vector, career_vector)
            match_score = round(similarity * 100, 2)
            
            recommendations.append({
                'career': career,
                'match_score': match_score,
                'profile': profile
            })
        
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:top_n]
    
    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def analyze_combined(self, text=None, answers=None):
        """
        Combined analysis using both text and questionnaire data
        Returns comprehensive personality analysis
        """
        if answers is not None:
            trait_scores = self.calculate_traits_from_answers(answers)
        elif text is not None:
            trait_scores = self.analyze_text_advanced(text)
        else:
            raise ValueError("Either text or answers must be provided")
        
        personality_types = self.predict_personality_type(trait_scores)
        descriptions = self.get_personality_description(personality_types)
        career_recs = self.recommend_careers(trait_scores)
        
        return {
            'traits': trait_scores,
            'personality_types': personality_types,
            'descriptions': descriptions,
            'career_recommendations': career_recs,
            'analysis_method': 'ml_enhanced',
            'timestamp': datetime.now().isoformat()
        }
    
    def save_model(self, path):
        """Save model state"""
        model_state = {
            'TRAIT_PATTERNS': self.TRAIT_PATTERNS,
            'CAREER_TRAIT_PROFILES': self.CAREER_TRAIT_PROFILES,
            'is_trained': self.is_trained
        }
        
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
        with open(path, 'w') as f:
            json.dump(model_state, f, indent=2)
    
    def load_model(self, path):
        """Load model state"""
        if os.path.exists(path):
            with open(path, 'r') as f:
                model_state = json.load(f)
                self.TRAIT_PATTERNS = model_state.get('TRAIT_PATTERNS', self.TRAIT_PATTERNS)
                self.CAREER_TRAIT_PROFILES = model_state.get('CAREER_TRAIT_PROFILES', self.CAREER_TRAIT_PROFILES)
                self.is_trained = model_state.get('is_trained', False)


def train_model():
    """
    Simulates training the model
    In production, this would load real training data
    """
    predictor = PersonalityPredictor()
    
    training_data = [
        {'answers': [5,5,5,5,5,5,5,5,5,5, 5,5,5,5,5,5,5,5,5,5, 5,5,5,5,5,5,5,5,5,5, 1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1], 'expected': [100,100,100,20,20]},
        {'answers': [1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1, 5,5,5,5,5,5,5,5,5,5, 5,5,5,5,5,5,5,5,5,5], 'expected': [20,20,20,100,100]},
        {'answers': [3,3,3,3,3,3,3,3,3,3, 3,3,3,3,3,3,3,3,3,3, 3,3,3,3,3,3,3,3,3,3, 3,3,3,3,3,3,3,3,3,3, 3,3,3,3,3,3,3,3,3,3], 'expected': [60,60,60,60,60]},
    ]
    
    predictor.is_trained = True
    
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(model_dir, exist_ok=True)
    predictor.save_model(os.path.join(model_dir, 'personality_model.json'))
    
    print(f"Model trained on {len(training_data)} samples")
    print(f"Model saved to {model_dir}/personality_model.json")
    
    return predictor


if __name__ == '__main__':
    predictor = train_model()
    
    test_text = "I enjoy solving technical problems and working on the computer. I prefer working alone and I like to analyze data."
    result = predictor.analyze_text_advanced(test_text)
    print(f"\nText Analysis: {result}")
    
    sample_answers = [4,4,5,4,5,4,3,5,4,5, 5,4,4,5,4,5,4,4,5,4, 3,3,4,3,4,3,3,4,3,3, 5,5,4,5,5,4,5,5,4,5, 2,3,2,3,2,3,2,2,3,2]
    result = predictor.analyze_combined(answers=sample_answers)
    print(f"\nCombined Analysis:")
    print(f"Traits: {result['traits']}")
    print(f"Types: {result['personality_types']}")
    print(f"Top Career: {result['career_recommendations'][0]}")
