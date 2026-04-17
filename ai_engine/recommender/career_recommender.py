class CareerRecommender:
    CAREER_PROFILES = {
        'Software Engineer': {
            'required_traits': {'openness': 60, 'conscientiousness': 70, 'extraversion': 40},
            'skills': ['Python', 'JavaScript', 'Data Structures', 'Algorithms', 'Git']
        },
        'Data Scientist': {
            'required_traits': {'openness': 70, 'conscientiousness': 60, 'extraversion': 35},
            'skills': ['Python', 'R', 'Machine Learning', 'Statistics', 'SQL']
        },
        'AI/ML Engineer': {
            'required_traits': {'openness': 80, 'conscientiousness': 65, 'extraversion': 30},
            'skills': ['Python', 'TensorFlow', 'PyTorch', 'Deep Learning', 'NLP']
        },
        'UX Designer': {
            'required_traits': {'openness': 80, 'conscientiousness': 50, 'extraversion': 55},
            'skills': ['Figma', 'User Research', 'Prototyping', 'Visual Design', 'Empathy']
        },
        'Project Manager': {
            'required_traits': {'conscientiousness': 80, 'extraversion': 60, 'agreeableness': 65},
            'skills': ['Agile', 'Scrum', 'Communication', 'Risk Management', 'Leadership']
        },
        'Marketing Manager': {
            'required_traits': {'extraversion': 75, 'openness': 60, 'agreeableness': 55},
            'skills': ['SEO', 'Content Marketing', 'Analytics', 'Social Media', 'Branding']
        },
        'Cybersecurity Analyst': {
            'required_traits': {'conscientiousness': 75, 'neuroticism': 45, 'openness': 55},
            'skills': ['Network Security', 'Penetration Testing', 'SIEM', 'Compliance', 'Incident Response']
        },
        'Research Scientist': {
            'required_traits': {'openness': 85, 'conscientiousness': 70, 'neuroticism': 40},
            'skills': ['Research Methods', 'Data Analysis', 'Scientific Writing', 'Statistics', 'Lab Work']
        },
        'Financial Analyst': {
            'required_traits': {'conscientiousness': 75, 'openness': 50, 'extraversion': 40},
            'skills': ['Financial Modeling', 'Excel', 'Data Analysis', 'Risk Assessment', 'Accounting']
        },
        'Teacher/Educator': {
            'required_traits': {'extraversion': 65, 'agreeableness': 80, 'conscientiousness': 60},
            'skills': ['Communication', 'Curriculum Design', 'Classroom Management', 'Patience', 'Adaptability']
        }
    }
    
    def __init__(self):
        pass
    
    def calculate_match_score(self, user_traits, career_traits):
        score = 0
        total_weight = 0
        
        for trait, required_value in career_traits.items():
            if trait in user_traits:
                user_value = user_traits[trait]
                difference = abs(user_value - required_value)
                
                if difference <= 10:
                    trait_score = 100 - difference
                else:
                    trait_score = max(0, 50 - difference)
                
                weight = 1.5 if trait in ['conscientiousness', 'openness'] else 1.0
                score += trait_score * weight
                total_weight += weight
        
        return round(score / total_weight, 2) if total_weight > 0 else 0
    
    def get_recommendations(self, user_traits):
        recommendations = []
        
        for career, profile in self.CAREER_PROFILES.items():
            match_score = self.calculate_match_score(user_traits, profile['required_traits'])
            
            if match_score >= 50:
                recommendations.append({
                    'name': career,
                    'match_score': match_score,
                    'skills': profile['skills'],
                    'description': f"{career} - Match: {match_score}%"
                })
        
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:5]
    
    def get_skills_for_career(self, career):
        if career in self.CAREER_PROFILES:
            return self.CAREER_PROFILES[career]['skills']
        return []
