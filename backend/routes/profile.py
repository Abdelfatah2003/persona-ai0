from flask import Blueprint, request, jsonify
from database.connection import get_db
from bson.objectid import ObjectId

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/<user_id>', methods=['GET'])
def get_profile(user_id):
    db = get_db()
    
    user = None
    if '@' in user_id:
        user = db.users.find_one({'email': user_id})
    else:
        try:
            user = db.users.find_one({'_id': ObjectId(user_id)})
        except:
            user = db.users.find_one({'email': user_id})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    email = user.get('email', user_id)
    personality = db.personalities.find_one({'user_email': email})
    recommendations = db.recommendations.find_one({'user_email': email})
    
    profile = {
        'user': {
            '_id': str(user['_id']),
            'name': user.get('name', ''),
            'email': user.get('email', ''),
            'age': user.get('age'),
            'goal': user.get('goal', ''),
            'created_at': str(user.get('created_at', ''))
        },
        'personality': None,
        'recommendations': None,
        'similar_users': []
    }
    
    if personality:
        profile['personality'] = {
            'openness': personality.get('openness', 0),
            'conscientiousness': personality.get('conscientiousness', 0),
            'extraversion': personality.get('extraversion', 0),
            'agreeableness': personality.get('agreeableness', 0),
            'neuroticism': personality.get('neuroticism', 0),
            'personality_type': personality.get('personality_type', ''),
            'updated_at': str(personality.get('updated_at', ''))
        }
    
    if recommendations:
        profile['recommendations'] = recommendations.get('careers', [])
        profile['similar_users'] = recommendations.get('similar_users', [])
    
    return jsonify(profile), 200

@profile_bp.route('/<user_id>', methods=['PUT'])
def update_profile(user_id):
    db = get_db()
    data = request.get_json()
    
    update_data = {}
    if 'name' in data:
        update_data['name'] = data['name']
    if 'goal' in data:
        update_data['goal'] = data['goal']
    if 'age' in data:
        update_data['age'] = data['age']
    
    if update_data:
        db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
    
    return jsonify({'message': 'Profile updated successfully'}), 200

@profile_bp.route('/<user_id>/history', methods=['GET'])
def get_history(user_id):
    db = get_db()
    
    histories = list(db.quiz_history.find({'user_id': user_id}).sort('created_at', -1).limit(10))
    
    result = []
    for history in histories:
        result.append({
            '_id': str(history['_id']),
            'traits': history.get('traits', {}),
            'careers': history.get('careers', []),
            'created_at': str(history.get('created_at', ''))
        })
    
    return jsonify({'history': result}), 200
