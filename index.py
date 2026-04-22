from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'API is running'})

@app.route('/')
def home():
    return 'Persona AI - Running!'