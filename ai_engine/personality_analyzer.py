import numpy as np

class PersonalityAnalyzer:
    TRAIT_NAMES = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
    
    TRAIT_PATTERNS = {
        'openness': ['creative', 'imagine', 'curious', 'art', 'new', 'idea', 'adventure', 'philosophy'],
        'conscientiousness': ['plan', 'organize', 'detail', 'deadline', 'reliable', 'discipline', 'goal'],
        'extraversion': ['social', 'talk', 'energy', 'party', 'friend', 'outgoing', 'team', 'attention'],
        'agreeableness': ['help', 'trust', 'kind', 'cooperate', 'forgive', 'sympathy', 'care'],
        'neuroticism': ['anxious', 'worry', 'stress', 'emotion', 'mood', 'nervous', 'sad']
    }
    
    def __init__(self):
        pass
    
    def calculate_traits(self, answers):
        if len(answers) != 50:
            raise ValueError("Expected 50 answers")
        
        openness = np.mean(answers[0:10]) * 20
        conscientiousness = np.mean(answers[10:20]) * 20
        extraversion = np.mean(answers[20:30]) * 20
        agreeableness = np.mean(answers[30:40]) * 20
        neuroticism = np.mean(answers[40:50]) * 20
        
        return {
            'openness': round(openness, 2),
            'conscientiousness': round(conscientiousness, 2),
            'extraversion': round(extraversion, 2),
            'agreeableness': round(agreeableness, 2),
            'neuroticism': round(neuroticism, 2)
        }
    
    def analyze_text(self, processed_text):
        text_lower = processed_text.lower()
        word_counts = {}
        
        for trait, keywords in self.TRAIT_PATTERNS.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            word_counts[trait] = count
        
        max_count = max(word_counts.values()) if max(word_counts.values()) > 0 else 1
        
        traits = {}
        for trait, count in word_counts.items():
            normalized_score = (count / max_count) * 80 + 20
            traits[trait] = round(normalized_score, 2)
        
        return traits
    
    def get_personality_type(self, traits):
        type_scores = []
        
        if traits['openness'] > 60:
            type_scores.append('Explorer')
        if traits['conscientiousness'] > 60:
            type_scores.append('Achiever')
        if traits['extraversion'] > 60:
            type_scores.append('Socializer')
        if traits['agreeableness'] > 60:
            type_scores.append('Helper')
        if traits['neuroticism'] > 60:
            type_scores.append('Thinker')
        
        if not type_scores:
            type_scores.append('Balanced')
        
        return ' & '.join(type_scores[:2]) if len(type_scores) > 1 else type_scores[0]
    
    def compare_traits(self, traits1, traits2):
        differences = []
        for trait in self.TRAIT_NAMES:
            diff = abs(traits1[trait] - traits2[trait])
            differences.append(diff)
        return np.mean(differences)
