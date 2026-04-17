from ai_engine.recommender.similarity import cosine_similarity
from database.connection import get_db
from bson import ObjectId

class UserRecommender:
    def __init__(self):
        self.db = get_db()
    
    def find_similar_users(self, user_email, user_traits, limit=5):
        all_personalities = list(self.db.personalities.find())
        
        user_vector = [
            float(user_traits.get('openness', 0)),
            float(user_traits.get('conscientiousness', 0)),
            float(user_traits.get('extraversion', 0)),
            float(user_traits.get('agreeableness', 0)),
            float(user_traits.get('neuroticism', 0))
        ]
        
        similarities = []
        
        for personality in all_personalities:
            personality_email = personality.get('user_email')
            
            if not personality_email:
                continue
            
            if personality_email == user_email:
                continue
            
            user_info = self.db.users.find_one({'email': personality_email})
            if not user_info:
                continue
            
            other_vector = [
                float(personality.get('openness', 0)),
                float(personality.get('conscientiousness', 0)),
                float(personality.get('extraversion', 0)),
                float(personality.get('agreeableness', 0)),
                float(personality.get('neuroticism', 0))
            ]
            
            sim = cosine_similarity(user_vector, other_vector)
            
            if sim > 0.3:
                name = user_info.get('name', 'Unknown')
                name_parts = name.split() if name else ['U']
                initials = ''.join([n[0] for n in name_parts if n])[:2].upper()
                
                similarities.append({
                    'user_id': personality_email,
                    'name': name,
                    'goal': user_info.get('goal', ''),
                    'initials': initials,
                    'similarity': round(sim * 100, 1),
                    'traits': {
                        'openness': personality.get('openness', 0),
                        'conscientiousness': personality.get('conscientiousness', 0),
                        'extraversion': personality.get('extraversion', 0),
                        'agreeableness': personality.get('agreeableness', 0),
                        'neuroticism': personality.get('neuroticism', 0)
                    }
                })
        
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:limit]
    
    def get_user_vectors(self):
        all_personalities = list(self.db.personalities.find())
        vectors = []
        user_ids = []
        
        for personality in all_personalities:
            vector = [
                float(personality.get('openness', 0)),
                float(personality.get('conscientiousness', 0)),
                float(personality.get('extraversion', 0)),
                float(personality.get('agreeableness', 0)),
                float(personality.get('neuroticism', 0))
            ]
            vectors.append(vector)
            user_ids.append(str(personality.get('user_email', '')))
        
        return vectors, user_ids
