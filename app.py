import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://render:A.m.z.55@cluster0.y4unpuc.mongodb.net/personaai?retryWrites=true&w=majority')

client = MongoClient(MONGO_URI)
db = client.get_default_database()
users_col = db['users']
personality_col = db['personalities']

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
    if traits.get("openness", 0) > 60: types.append("Explorer")
    if traits.get("conscientiousness", 0) > 60: types.append("Achiever")
    if traits.get("extraversion", 0) > 60: types.append("Socializer")
    if traits.get("agreeableness", 0) > 60: types.append("Helper")
    if traits.get("neuroticism", 0) < 40: types.append("Stabilizer")
    return " & ".join(types) if types else "Balanced"

def get_career_recommendations(traits):
    careers = []
    o, c, e, a = traits.get("openness", 0), traits.get("conscientiousness", 0), traits.get("extraversion", 0), traits.get("agreeableness", 0)
    if o > 50: careers.append({"name": "Data Scientist", "match_score": 92, "description": "Analyze data and build predictive models", "skills": ["Python", "Machine Learning"]})
    if c > 50: careers.append({"name": "Software Engineer", "match_score": 88, "description": "Design and build software solutions", "skills": ["JavaScript", "Python"]})
    if o > 60 and c > 60: careers.append({"name": "AI/ML Engineer", "match_score": 90, "description": "Develop AI systems", "skills": ["TensorFlow", "Deep Learning"]})
    if e > 60: careers.append({"name": "Product Manager", "match_score": 85, "description": "Lead product development", "skills": ["Leadership", "Strategy"]})
    if a > 60: careers.append({"name": "UX Designer", "match_score": 82, "description": "Design user experiences", "skills": ["Design", "Empathy"]})
    return careers[:4] or [{"name": "Generalist", "match_score": 70, "description": "Versatile role", "skills": ["Communication"]}]

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(BASE_DIR, filename)

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'version': '2.0.0'})

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email', '').lower()
    password = data.get('password', '')
    name = data.get('name', email.split('@')[0])
    
    if users_col.find_one({'email': email}):
        return jsonify({'error': 'Email already registered'}), 400
    
    user_id = users_col.insert_one({'email': email, 'password': password, 'name': name}).inserted_id
    return jsonify({'success': True, 'user': {'id': str(user_id), 'email': email, 'name': name}})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').lower()
    password = data.get('password', '')
    
    user = users_col.find_one({'email': email, 'password': password})
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({'success': True, 'user': {'id': str(user['_id']), 'email': user['email'], 'name': user['name']}})

@app.route('/api/auth/user/<email>')
def get_user(email):
    user = users_col.find_one({'email': email.lower()})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'success': True, 'user': {'id': str(user['_id']), 'email': user['email'], 'name': user['name']}})

@app.route('/api/personality/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    answers = data.get('answers', [])
    if len(answers) != 50:
        return jsonify({'error': 'Need 50 answers'}), 400
    traits = calculate_traits(answers)
    return jsonify({'success': True, 'traits': traits, 'personality_type': get_personality_type(traits)})

@app.route('/api/personality/save', methods=['POST'])
def save_personality():
    data = request.get_json()
    email = data.get('email', '').lower()
    traits = data.get('traits', {})
    
    personality_col.update_one(
        {'email': email},
        {'$set': {'email': email, 'traits': traits, 'personality_type': get_personality_type(traits)}},
        upsert=True
    )
    return jsonify({'success': True})

@app.route('/api/personality/get/<email>')
def get_personality(email):
    pers = personality_col.find_one({'email': email.lower()})
    if not pers:
        return jsonify({'error': 'Not found', 'personality': None}), 404
    return jsonify({'success': True, 'personality': {'email': pers['email'], 'traits': pers['traits'], 'personality_type': pers.get('personality_type', 'Balanced')}})

@app.route('/api/recommendations/careers', methods=['POST'])
def careers():
    traits = request.get_json().get('traits', {})
    return jsonify({'success': True, 'careers': get_career_recommendations(traits)})

@app.route('/api/recommendations/users/<email>')
def similar_users(email):
    current = personality_col.find_one({'email': email.lower()})
    if not current:
        return jsonify({'error': 'User not found'}), 404
    
    similar = []
    for pers in personality_col.find({'email': {'$ne': email.lower()}}):
        c_t = current.get('traits', {})
        o_t = pers.get('traits', {})
        sim = max(0, 100 - abs(c_t.get('openness', 0) - o_t.get('openness', 0)) * 0.5)
        if sim > 70:
            user = users_col.find_one({'email': pers['email']})
            similar.append({'email': pers['email'], 'name': user['name'] if user else pers['email'], 'similarity': round(sim), **o_t})
    
    return jsonify({'success': True, 'similar_users': sorted(similar, key=lambda x: x['similarity'], reverse=True)[:5]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)