"""
Enhanced Security Module with JWT, Rate Limiting, and Input Validation
"""
import re
import time
import secrets
from functools import wraps
from datetime import datetime, timedelta
from flask import request, jsonify, g, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bcrypt
import jwt


class SecurityManager:
    """Handles all security-related functionality"""
    
    def __init__(self, app=None):
        self.app = app
        self.rate_limiter = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize security features"""
        self.app = app
        
        # Initialize rate limiter
        self.rate_limiter = Limiter(
            key_func=get_remote_address,
            app=app,
            default_limits=["200 per day", "50 per hour"],
            storage_uri="memory://" if app.config.get('TESTING') else "memory://",
            strategy="fixed-window"
        )
        
        # Register error handlers
        @app.errorhandler(429)
        def ratelimit_handler(e):
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests. Please try again later.',
                'retry_after': e.description
            }), 429
        
        @app.errorhandler(401)
        def unauthorized_handler(e):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required'
            }), 401
    
    def generate_token(self, user_id, email, expires_in=7):
        """Generate JWT token"""
        secret = current_app.config.get('JWT_SECRET_KEY', 'secret')
        payload = {
            'user_id': user_id,
            'email': email,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=expires_in),
            'jti': secrets.token_hex(16)
        }
        return jwt.encode(payload, secret, algorithm='HS256')
    
    def verify_token(self, token):
        """Verify JWT token"""
        try:
            secret = current_app.config.get('JWT_SECRET_KEY', 'secret')
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def hash_password(self, password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password, hashed):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_reset_token(self):
        """Generate password reset token"""
        return secrets.token_urlsafe(32)
    
    def generate_verification_token(self):
        """Generate email verification token"""
        return secrets.token_urlsafe(48)


security_manager = SecurityManager()


def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = security_manager.verify_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        g.current_user = payload
        return f(*args, **kwargs)
    
    return decorated


def rate_limit(limit="10 per minute"):
    """Decorator to apply specific rate limit"""
    def decorator(f):
        return security_manager.rate_limiter.limit(limit)(f)
    return decorator


class InputValidator:
    """Input validation utilities"""
    
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email or not isinstance(email, str):
            return False, "Email is required"
        if not InputValidator.EMAIL_REGEX.match(email):
            return False, "Invalid email format"
        if len(email) > 254:
            return False, "Email too long"
        return True, None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if not password or not isinstance(password, str):
            return False, "Password is required"
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if len(password) > 128:
            return False, "Password too long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain number"
        return True, None
    
    @staticmethod
    def validate_name(name):
        """Validate name format"""
        if not name or not isinstance(name, str):
            return False, "Name is required"
        if len(name) < 2:
            return False, "Name too short"
        if len(name) > 100:
            return False, "Name too long"
        if not re.match(r'^[a-zA-Z\s\'-]+$', name):
            return False, "Name contains invalid characters"
        return True, None
    
    @staticmethod
    def validate_age(age):
        """Validate age"""
        if age is None:
            return True, None  # Age is optional
        try:
            age = int(age)
            if age < 10 or age > 120:
                return False, "Age must be between 10 and 120"
            return True, None
        except (ValueError, TypeError):
            return False, "Invalid age format"
    
    @staticmethod
    def validate_quiz_answers(answers):
        """Validate quiz answers"""
        if not answers or not isinstance(answers, list):
            return False, "Answers must be a list"
        if len(answers) != 50:
            return False, "Exactly 50 answers required"
        for i, answer in enumerate(answers):
            try:
                answer = int(answer)
                if answer < 1 or answer > 5:
                    return False, f"Answer {i+1} must be between 1 and 5"
            except (ValueError, TypeError):
                return False, f"Answer {i+1} must be a number"
        return True, None
    
    @staticmethod
    def validate_text_input(text, min_length=10, max_length=5000):
        """Validate text input for analysis"""
        if not text or not isinstance(text, str):
            return False, "Text is required"
        text = text.strip()
        if len(text) < min_length:
            return False, f"Text must be at least {min_length} characters"
        if len(text) > max_length:
            return False, f"Text must not exceed {max_length} characters"
        return True, None
    
    @staticmethod
    def sanitize_input(text):
        """Sanitize user input to prevent XSS"""
        if not text:
            return ""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove script-like patterns
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)
        return text.strip()


def validate_request(required_fields=None, optional_fields=None):
    """Decorator to validate request data"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data = request.get_json() or {}
            
            # Validate required fields
            if required_fields:
                for field in required_fields:
                    if field not in data or data[field] is None:
                        return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Validate email
            if 'email' in data:
                valid, error = InputValidator.validate_email(data['email'])
                if not valid:
                    return jsonify({'error': error}), 400
            
            # Validate password (for registration)
            if 'password' in data and request.endpoint and 'register' in request.endpoint:
                valid, error = InputValidator.validate_password(data['password'])
                if not valid:
                    return jsonify({'error': error}), 400
            
            # Validate name
            if 'name' in data:
                valid, error = InputValidator.validate_name(data['name'])
                if not valid:
                    return jsonify({'error': error}), 400
            
            # Validate age
            if 'age' in data:
                valid, error = InputValidator.validate_age(data['age'])
                if not valid:
                    return jsonify({'error': error}), 400
            
            # Validate quiz answers
            if 'answers' in data:
                valid, error = InputValidator.validate_quiz_answers(data['answers'])
                if not valid:
                    return jsonify({'error': error}), 400
            
            # Validate text
            if 'text' in data:
                valid, error = InputValidator.validate_text_input(data['text'])
                if not valid:
                    return jsonify({'error': error}), 400
            
            return f(*args, **kwargs)
        return decorated
    return decorator
