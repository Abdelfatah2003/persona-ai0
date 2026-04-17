from flask import Blueprint, request, jsonify
from database.connection import get_db
from ai_engine.recommender.career_recommender import CareerRecommender
from ai_engine.recommender.user_recommender import UserRecommender

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/careers', methods=['POST'])
def get_career_recommendations():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Traits data required'}), 400
    
    recommender = CareerRecommender()
    careers = recommender.get_recommendations(data)
    
    return jsonify({'careers': careers}), 200

@recommendations_bp.route('/users', methods=['POST'])
def get_similar_users():
    data = request.get_json()
    
    user_id = data.get('userId')
    traits = data.get('traits', {})
    
    if not user_id:
        return jsonify({'error': 'User ID required'}), 400
    
    recommender = UserRecommender()
    similar_users = recommender.find_similar_users(user_id, traits)
    
    return jsonify({'similar_users': similar_users}), 200

@recommendations_bp.route('/skills/<career>', methods=['GET'])
def get_skills_for_career(career):
    db = get_db()
    career_doc = db.careers.find_one({'name': career})
    
    if career_doc:
        return jsonify({'skills': career_doc.get('skills', [])}), 200
    
    return jsonify({'skills': []}), 200

@recommendations_bp.route('/similar-users/<user_id>', methods=['GET'])
def get_similar_users_by_id(user_id):
    db = get_db()
    
    from bson import ObjectId
    import urllib.parse
    
    user_id = urllib.parse.unquote(user_id)
    
    if '@' in user_id:
        personality = db.personalities.find_one({'user_email': user_id})
    else:
        try:
            user_oid = ObjectId(user_id)
            personality = db.personalities.find_one({'_id': user_oid})
        except:
            return jsonify({'error': 'Invalid user ID', 'received': user_id}), 400
    
    if not personality:
        return jsonify({
            'error': 'User personality not found', 
            'received_user_id': user_id,
            'hint': 'User must complete the quiz first'
        }), 404
    
    traits = {
        'openness': personality.get('openness', 0),
        'conscientiousness': personality.get('conscientiousness', 0),
        'extraversion': personality.get('extraversion', 0),
        'agreeableness': personality.get('agreeableness', 0),
        'neuroticism': personality.get('neuroticism', 0)
    }
    
    recommender = UserRecommender()
    user_key = user_id if '@' in user_id else personality.get('user_email')
    similar_users = recommender.find_similar_users(user_key, traits)
    
    return jsonify({'similar_users': similar_users}), 200

@recommendations_bp.route('/debug', methods=['GET'])
def debug_recommendations():
    db = get_db()
    
    users_count = db.users.count_documents({})
    personalities_count = db.personalities.count_documents({})
    
    personalities = list(db.personalities.find({}, {'_id': 0, 'user_email': 1, 'openness': 1, 'conscientiousness': 1}))
    
    return jsonify({
        'users_count': users_count,
        'personalities_count': personalities_count,
        'personalities': personalities
    }), 200
