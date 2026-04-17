from datetime import datetime

class Personality:
    def __init__(self, user_id, openness, conscientiousness, extraversion, agreeableness, neuroticism):
        self.user_id = user_id
        self.openness = openness
        self.conscientiousness = conscientiousness
        self.extraversion = extraversion
        self.agreeableness = agreeableness
        self.neuroticism = neuroticism
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'openness': self.openness,
            'conscientiousness': self.conscientiousness,
            'extraversion': self.extraversion,
            'agreeableness': self.agreeableness,
            'neuroticism': self.neuroticism,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def get_traits_array(self):
        return [self.openness, self.conscientiousness, self.extraversion, self.agreeableness, self.neuroticism]

class PersonalityModel:
    def __init__(self, db):
        self.collection = db.personalities
    
    def save(self, personality):
        personality.updated_at = datetime.utcnow()
        self.collection.update_one(
            {'user_id': personality.user_id},
            {'$set': personality.to_dict()},
            upsert=True
        )
    
    def find_by_user_id(self, user_id):
        return self.collection.find_one({'user_id': user_id})
    
    def get_all(self):
        return list(self.collection.find())
    
    def delete(self, user_id):
        self.collection.delete_one({'user_id': user_id})
