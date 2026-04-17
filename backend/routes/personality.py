"""
Enhanced Personality Routes with ML Integration
"""
from flask import Blueprint, request, jsonify, g
from database.connection import get_db
from ai_engine.personality_analyzer import PersonalityAnalyzer
from ai_engine.text_processor import TextProcessor
from ai_engine.ml_predictor import PersonalityPredictor
from backend.security import InputValidator, validate_request, rate_limit, token_required
from backend.logging_config import audit_logger
from datetime import datetime

personality_bp = Blueprint('personality', __name__)


@personality_bp.route('/analyze', methods=['POST'])
@rate_limit("30 per minute")
@validate_request(['answers'])
def analyze_personality():
    """Analyze personality from quiz answers"""
    data = request.get_json()
    answers = data.get('answers', [])
    
    # Validate answers
    valid, error = InputValidator.validate_quiz_answers(answers)
    if not valid:
        return jsonify({'error': error}), 400
    
    analyzer = PersonalityAnalyzer()
    traits = analyzer.calculate_traits(answers)
    
    # Also get ML-based predictions for comparison
    ml_predictor = PersonalityPredictor()
    ml_traits = ml_predictor.calculate_traits_from_answers(answers)
    ml_types = ml_predictor.predict_personality_type(ml_traits)
    
    return jsonify({
        'traits': traits,
        'personality_type': analyzer.get_personality_type(traits),
        'ml_predictions': {
            'traits': ml_traits,
            'types': ml_types,
            'descriptions': ml_predictor.get_personality_description(ml_types)
        }
    }), 200


@personality_bp.route('/analyze-text', methods=['POST'])
@rate_limit("30 per minute")
@validate_request(['text'])
def analyze_text():
    """Analyze personality from free text"""
    data = request.get_json()
    text = data.get('text', '')
    
    # Validate text
    valid, error = InputValidator.validate_text_input(text, min_length=20)
    if not valid:
        return jsonify({'error': error}), 400
    
    # Sanitize input
    text = InputValidator.sanitize_input(text)
    
    processor = TextProcessor()
    processed_text = processor.preprocess(text)
    
    analyzer = PersonalityAnalyzer()
    traits = analyzer.analyze_text(processed_text)
    
    # Get ML-based analysis
    ml_predictor = PersonalityPredictor()
    ml_traits = ml_predictor.analyze_text_advanced(text)
    ml_types = ml_predictor.predict_personality_type(ml_traits)
    
    keywords = processor.extract_keywords(processed_text)
    
    return jsonify({
        'traits': traits,
        'personality_type': analyzer.get_personality_type(traits),
        'ml_predictions': {
            'traits': ml_traits,
            'types': ml_types,
            'descriptions': ml_predictor.get_personality_description(ml_types)
        },
        'keywords': keywords[:10]
    }), 200


@personality_bp.route('/save', methods=['POST'])
@rate_limit("10 per minute")
def save_personality():
    """Save personality analysis results"""
    data = request.get_json()
    
    email = data.get('email')
    answers = data.get('answers', [])
    traits = data.get('traits', {})
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Validate email
    valid, error = InputValidator.validate_email(email)
    if not valid:
        return jsonify({'error': error}), 400
    
    db = get_db()
    
    user = db.users.find_one({'email': email})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Use ML predictor for comprehensive analysis
    ml_predictor = PersonalityPredictor()
    
    if answers:
        # Calculate from answers
        calculated_traits = ml_predictor.calculate_traits_from_answers(answers)
        personality_types = ml_predictor.predict_personality_type(calculated_traits)
    else:
        # Use provided traits
        calculated_traits = traits
        personality_types = ml_predictor.predict_personality_type(traits)
    
    # Prepare personality data
    personality_data = {
        'user_email': email,
        'user_id': str(user.get('_id')),
        'openness': float(calculated_traits.get('openness', 0)),
        'conscientiousness': float(calculated_traits.get('conscientiousness', 0)),
        'extraversion': float(calculated_traits.get('extraversion', 0)),
        'agreeableness': float(calculated_traits.get('agreeableness', 0)),
        'neuroticism': float(calculated_traits.get('neuroticism', 0)),
        'personality_type': ' & '.join(personality_types[:2]),
        'personality_types': personality_types,
        'answers': answers if answers else [],
        'updated_at': datetime.utcnow()
    }
    
    if not db.personalities.find_one({'user_email': email}):
        personality_data['created_at'] = datetime.utcnow()
    
    db.personalities.update_one(
        {'user_email': email},
        {'$set': personality_data},
        upsert=True
    )
    
    audit_logger.log_quiz_completed(email, calculated_traits)
    
    return jsonify({
        'message': 'Personality saved successfully',
        'personality_type': personality_data['personality_type'],
        'personality_types': personality_types,
        'traits': {
            'openness': personality_data['openness'],
            'conscientiousness': personality_data['conscientiousness'],
            'extraversion': personality_data['extraversion'],
            'agreeableness': personality_data['agreeableness'],
            'neuroticism': personality_data['neuroticism']
        }
    }), 200


@personality_bp.route('/get/<user_id>', methods=['GET'])
def get_personality(user_id):
    """Get personality by user ID or email"""
    db = get_db()
    
    import urllib.parse
    user_id = urllib.parse.unquote(user_id)
    
    if '@' in user_id:
        personality = db.personalities.find_one({'user_email': user_id})
    else:
        personality = db.personalities.find_one({'user_id': user_id})
    
    if not personality:
        return jsonify({'error': 'Personality not found'}), 404
    
    personality['_id'] = str(personality['_id'])
    return jsonify(personality), 200


@personality_bp.route('/history/<email>', methods=['GET'])
def get_personality_history(email):
    """Get personality analysis history"""
    import urllib.parse
    email = urllib.parse.unquote(email)
    
    db = get_db()
    
    # Get all personality records for user
    history = list(db.personalities.find(
        {'user_email': email},
        {'_id': 0, 'user_email': 1, 'traits': 1, 'personality_type': 1, 'created_at': 1}
    ).sort('created_at', -1).limit(10))
    
    return jsonify({'history': history}), 200


@personality_bp.route('/compare', methods=['POST'])
@token_required
def compare_personalities():
    """Compare two users' personalities"""
    data = request.get_json()
    
    email1 = data.get('email1')
    email2 = data.get('email2')
    
    if not email1 or not email2:
        return jsonify({'error': 'Both emails are required'}), 400
    
    db = get_db()
    
    p1 = db.personalities.find_one({'user_email': email1})
    p2 = db.personalities.find_one({'user_email': email2})
    
    if not p1 or not p2:
        return jsonify({'error': 'One or both personalities not found'}), 404
    
    # Calculate differences
    from ai_engine.personality_analyzer import PersonalityAnalyzer
    analyzer = PersonalityAnalyzer()
    
    traits1 = {
        'openness': p1.get('openness', 0),
        'conscientiousness': p1.get('conscientiousness', 0),
        'extraversion': p1.get('extraversion', 0),
        'agreeableness': p1.get('agreeableness', 0),
        'neuroticism': p1.get('neuroticism', 0)
    }
    
    traits2 = {
        'openness': p2.get('openness', 0),
        'conscientiousness': p2.get('conscientiousness', 0),
        'extraversion': p2.get('extraversion', 0),
        'agreeableness': p2.get('agreeableness', 0),
        'neuroticism': p2.get('neuroticism', 0)
    }
    
    avg_diff = analyzer.compare_traits(traits1, traits2)
    similarity = max(0, 100 - avg_diff)
    
    return jsonify({
        'user1': {'email': email1, 'traits': traits1},
        'user2': {'email': email2, 'traits': traits2},
        'similarity_score': round(similarity, 2),
        'average_difference': round(avg_diff, 2)
    }), 200
