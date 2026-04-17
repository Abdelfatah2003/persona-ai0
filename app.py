import os
from flask import Flask, jsonify, send_from_directory, request, g
from flask_cors import CORS
from database.connection import init_db
from backend.routes.auth import auth_bp
from backend.routes.personality import personality_bp
from backend.routes.recommendations import recommendations_bp
from backend.routes.profile import profile_bp
from backend.security import SecurityManager, rate_limit
from backend.logging_config import setup_logging, RequestLogger
from dotenv import load_dotenv
import time
import logging

load_dotenv()

app = Flask(__name__)

app.config.from_object('backend.config.Config')

CORS(app, 
     resources={r"/api/*": {"origins": "*"}},
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

security_manager = SecurityManager(app)
logger = setup_logging(app, log_level=app.config.get('LOG_LEVEL', 'INFO'))

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - g.get('start_time', time.time())
    logger.info(f"{request.method} {request.path} | Status: {response.status_code} | Duration: {duration:.3f}s")
    return response

init_db()

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(personality_bp, url_prefix='/api/personality')
app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
app.register_blueprint(profile_bp, url_prefix='/api/profile')

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend', filename)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'API is running',
        'version': '2.0.0',
        'platform': 'vercel'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
