from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)