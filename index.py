from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.')

CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'API is running', 'version': '2.0.0'})

@app.route('/api/auth/register', methods=['POST'])
def register():
    return jsonify({'message': 'Registration endpoint - configure full API to use'}), 501

@app.route('/api/auth/login', methods=['POST'])
def login():
    return jsonify({'message': 'Login endpoint - configure full API to use'}), 501

@app.route('/api/personality/analyze', methods=['POST'])
def analyze():
    return jsonify({'message': 'Analyze endpoint - configure full API to use'}), 501

@app.route('/api/personality/analyze-text', methods=['POST'])
def analyze_text():
    return jsonify({'message': 'Analyze text endpoint - configure full API to use'}), 501

@app.route('/api/personality/save', methods=['POST'])
def save_personality():
    return jsonify({'message': 'Save endpoint - configure full API to use'}), 501

@app.route('/api/recommendations/careers', methods=['POST'])
def careers():
    return jsonify({'message': 'Careers endpoint - configure full API to use'}), 501

@app.route('/api/recommendations/users', methods=['POST'])
def users():
    return jsonify({'message': 'Users endpoint - configure full API to use'}), 501

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)