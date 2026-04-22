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

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'API is running', 'version': '2.0.0', 'platform': 'vercel'})

@app.route('/api/auth/register', methods=['POST'])
def register():
    return jsonify({'message': 'Setup full backend'}), 501

@app.route('/api/auth/login', methods=['POST'])  
def login():
    return jsonify({'message': 'Setup full backend'}), 501

@app.route('/api/personality/analyze', methods=['POST'])
def analyze():
    return jsonify({'message': 'Setup full backend'}), 501

@app.route('/api/personality/analyze-text', methods=['POST'])
def analyze_text():
    return jsonify({'message': 'Setup full backend'}), 501

@app.route('/api/personality/save', methods=['POST'])
def save_personality():
    return jsonify({'message': 'Setup full backend'}), 501

@app.route('/api/recommendations/careers', methods=['POST'])
def careers():
    return jsonify({'message': 'Setup full backend'}), 501

@app.route('/api/recommendations/users', methods=['POST'])
def users():
    return jsonify({'message': 'Setup full backend'}), 501