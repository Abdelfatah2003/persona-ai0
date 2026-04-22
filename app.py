import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

users_db = {}
personality_db = {}

def calculate_traits(answers):
    return {
        "openness": round(sum(answers[0:10]) / 10 * 20, 1),
        "conscientiousness": round(sum(answers[10:20]) / 10 * 20, 1),
        "extraversion": round(sum(answers[20:30]) / 10 * 20, 1),
        "agreeableness": round(sum(answers[30:40]) / 10 * 20, 1),
        "neuroticism": round(sum(answers[40:50]) / 10 * 20, 1)
    }

def get_personality_type(traits):
    types = []
    if traits.get("openness", 0) > 60:
        types.append("Explorer")
    if traits.get("conscientiousness", 0) > 60:
        types.append("Achiever")
    if traits.get("extraversion", 0) > 60:
        types.append("Socializer")
    if traits.get("agreeableness", 0) > 60:
        types.append("Helper")
    if traits.get("neuroticism", 0) < 40:
        types.append("Stabilizer")
    return " & ".join(types) if types else "Balanced"

def get_career_recommendations(traits):
    careers = []
    openness = traits.get("openness", 0)
    conscientiousness = traits.get("conscientiousness", 0)
    extraversion = traits.get("extraversion", 0)
    agreeableness = traits.get("agreeableness", 0)
    
    if openness > 50:
        careers.append({"name": "Data Scientist", "description": "Analyze data and build predictive models", "match_score": 92, "skills": ["Python", "Machine Learning", "Statistics"]})
    if conscientiousness > 50:
        careers.append({"name": "Software Engineer", "description": "Design and build software solutions", "match_score": 88, "skills": ["Python", "JavaScript", "Data Structures"]})
    if openness > 60 and conscientiousness > 60:
        careers.append({"name": "AI/ML Engineer", "description": "Develop artificial intelligence systems", "match_score": 90, "skills": ["Deep Learning", "TensorFlow", "NLP"]})
    if extraversion > 60:
        careers.append({"name": "Product Manager", "description": "Lead product development", "match_score": 85, "skills": ["Leadership", "Communication", "Strategy"]})
    if agreeableness > 60:
        careers.append({"name": "UX Designer", "description": "Design user experiences", "match_score": 82, "skills": ["Design", "Empathy", "Research"]})
    if not careers:
        careers.append({"name": "Generalist", "description": "Versatile role", "match_score": 70, "skills": ["Communication", "Problem Solving"]})
    return [{"name": c["name"], "description": c["description"], "match_score": c["match_score"], "skills": c["skills"]} for c in careers[:4]]

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(BASE_DIR, filename)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'API is running', 'version': '2.0.0'})

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email', '').lower()
    password = data.get('password', '')
    name = data.get('name', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    if email in users_db:
        return jsonify({'error': 'Email already registered'}), 400
    
    user_id = f"user_{len(users_db) + 1}"
    users_db[email] = {
        'id': user_id,
        'email': email,
        'password': password,
        'name': name or email.split('@')[0]
    }
    
    return jsonify({
        'success': True,
        'user': {'id': user_id, 'email': email, 'name': name},
        'token': f"token_{user_id}"
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').lower()
    password = data.get('password', '')
    
    user = users_db.get(email)
    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({
        'success': True,
        'user': {'id': user['id'], 'email': user['email'], 'name': user['name']},
        'token': f"token_{user['id']}"
    })

@app.route('/api/personality/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    answers = data.get('answers', [])
    
    if len(answers) != 50:
        return jsonify({'error': 'Need 50 answers'}), 400
    
    traits = calculate_traits(answers)
    personality_type = get_personality_type(traits)
    
    return jsonify({
        'success': True,
        'traits': traits,
        'personality_type': personality_type
    })

@app.route('/api/personality/analyze-text', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get('text', '')
    
    word_count = len(text.split())
    text_length = len(text)
    
    traits = {
        "openness": min(100, 50 + (text_length // 100)),
        "conscientiousness": min(100, 50 + (word_count // 10)),
        "extraversion": min(100, 50 + (text.count('!') + text.count(',')) * 5),
        "agreeableness": min(100, 50 + (text.lower().count('we') + text.lower().count('together')) * 3),
        "neuroticism": max(0, 50 - text.count('worried'))
    }
    personality_type = get_personality_type(traits)
    
    return jsonify({
        'success': True,
        'traits': traits,
        'personality_type': personality_type,
        'analysis': {'word_count': word_count, 'text_length': text_length}
    })

@app.route('/api/personality/save', methods=['POST'])
def save_personality():
    data = request.get_json()
    email = data.get('email', '').lower()
    traits = data.get('traits', {})
    
    if not email:
        return jsonify({'error': 'Email required'}), 400
    
    personality_db[email] = {
        'email': email,
        'traits': traits,
        'personality_type': get_personality_type(traits)
    }
    
    return jsonify({'success': True, 'message': 'Personality saved'})

@app.route('/api/personality/get/<email>', methods=['GET'])
def get_personality(email):
    email = email.lower()
    personality = personality_db.get(email)
    
    if not personality:
        return jsonify({'error': 'No personality found', 'personality': None}), 404
    
    return jsonify({
        'success': True,
        'personality': personality
    })

@app.route('/api/recommendations/careers', methods=['POST'])
def careers():
    data = request.get_json()
    traits = data.get('traits', {})
    
    if not traits:
        return jsonify({'error': 'Traits required'}), 400
    
    recommendations = get_career_recommendations(traits)
    
    return jsonify({
        'success': True,
        'careers': recommendations
    })

@app.route('/api/recommendations/users/<email>', methods=['GET'])
def similar_users(email):
    email = email.lower()
    current_personality = personality_db.get(email)
    
    if not current_personality:
        return jsonify({'error': 'User not found'}), 404
    
    similar = []
    for user_email, pers in personality_db.items():
        if user_email != email:
            current_traits = current_personality.get('traits', {})
            other_traits = pers.get('traits', {})
            similarity = 100 - abs(current_traits.get('openness', 0) - other_traits.get('openness', 0)) * 0.5
            if similarity > 70:
                similar.append({
                    'email': user_email,
                    'name': users_db.get(user_email, {}).get('name', user_email.split('@')[0]),
                    'similarity': round(similarity, 1),
                    'traits': other_traits
                })
    
    return jsonify({
        'success': True,
        'similar_users': sorted(similar, key=lambda x: x['similarity'], reverse=True)[:5]
    })

@app.route('/api/auth/user/<email>', methods=['GET'])
def get_user(email):
    email = email.lower()
    user = users_db.get(email)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'user': {'id': user['id'], 'email': user['email'], 'name': user['name']}
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)