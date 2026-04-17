from datetime import datetime

class Recommendation:
    def __init__(self, user_id, careers, similar_users):
        self.user_id = user_id
        self.careers = careers
        self.similar_users = similar_users
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'careers': self.careers,
            'similar_users': self.similar_users,
            'created_at': self.created_at
        }

class RecommendationModel:
    def __init__(self, db):
        self.collection = db.recommendations
    
    def save(self, recommendation):
        self.collection.update_one(
            {'user_id': recommendation.user_id},
            {'$set': recommendation.to_dict()},
            upsert=True
        )
    
    def find_by_user_id(self, user_id):
        return self.collection.find_one({'user_id': user_id})
    
    def delete(self, user_id):
        self.collection.delete_one({'user_id': user_id})
