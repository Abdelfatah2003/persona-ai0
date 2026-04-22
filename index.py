from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Persona AI'

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/test')
def test():
    return jsonify({'test': 'ok'})