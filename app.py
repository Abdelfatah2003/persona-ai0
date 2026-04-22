import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    return jsonify({'message': 'Register endpoint - configure database'}), 501

@app.route('/api/auth/login', methods=['POST'])
def login():
    return jsonify({'message': 'Login endpoint - configure database'}), 501

@app.route('/api/personality/analyze', methods=['POST'])
def analyze():
    return jsonify({'message': 'Personality analyze - configure ML'}), 501

@app.route('/api/personality/analyze-text', methods=['POST'])
def analyze_text():
    return jsonify({'message': 'Text analysis - configure NLP'}), 501

@app.route('/api/personality/save', methods=['POST'])
def save_personality():
    return jsonify({'message': 'Save personality - configure database'}), 501

@app.route('/api/recommendations/careers', methods=['POST'])
def careers():
    return jsonify({'message': 'Career recommendations - configure recommender'}), 501

@app.route('/api/recommendations/users', methods=['POST'])
def users():
    return jsonify({'message': 'Similar users - configure database'}), 501

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)