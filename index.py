from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Persona AI - Running!'

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'API is running'})