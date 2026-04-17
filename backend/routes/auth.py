"""
Enhanced Authentication Routes with Security Features
"""
from flask import Blueprint, request, jsonify
from database.connection import get_db
from backend.models.user import UserModel
from backend.security import (
    security_manager, InputValidator, 
    validate_request, rate_limit,
    token_required
)
from backend.logging_config import audit_logger
from backend.email_service import email_service
import bcrypt
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
@rate_limit("5 per minute")
@validate_request(['name', 'email', 'password'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Additional validation
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password')
    age = data.get('age')
    goal = data.get('goal', '').strip()
    
    # Validate name
    valid, error = InputValidator.validate_name(name)
    if not valid:
        return jsonify({'error': error}), 400
    
    # Validate email
    valid, error = InputValidator.validate_email(email)
    if not valid:
        return jsonify({'error': error}), 400
    
    # Validate password
    valid, error = InputValidator.validate_password(password)
    if not valid:
        return jsonify({'error': error}), 400
    
    # Validate age if provided
    if age is not None:
        valid, error = InputValidator.validate_age(age)
        if not valid:
            return jsonify({'error': error}), 400
    
    db = get_db()
    users = db.users
    
    # Check if user exists
    if users.find_one({'email': email}):
        audit_logger.log_registration(email, False)
        return jsonify({'error': 'Email already registered'}), 409
    
    # Hash password
    hashed_password = security_manager.hash_password(password)
    
    # Create user document
    user_data = {
        'name': InputValidator.sanitize_input(name),
        'email': email,
        'age': age,
        'goal': InputValidator.sanitize_input(goal) if goal else '',
        'password': hashed_password,
        'email_verified': False,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    try:
        result = users.insert_one(user_data)
        user_id = str(result.inserted_id)
        
        # Generate JWT token
        token = security_manager.generate_token(user_id, email)
        
        # Create user response (without password)
        user_response = {
            '_id': user_id,
            'name': user_data['name'],
            'email': email,
            'age': age,
            'goal': user_data['goal']
        }
        
        audit_logger.log_registration(email, True)
        
        # Send welcome email (async in production)
        try:
            email_service.send_welcome_email(email, user_data['name'])
        except Exception as e:
            # Log but don't fail registration
            import logging
            logging.getLogger().warning(f"Failed to send welcome email: {e}")
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user_response,
            'token': token
        }), 201
        
    except Exception as e:
        import logging
        logging.getLogger().error(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500


@auth_bp.route('/login', methods=['POST'])
@rate_limit("10 per minute")
@validate_request(['email', 'password'])
def login():
    """Authenticate user and return JWT token"""
    data = request.get_json()
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    ip_address = request.remote_addr
    
    # Validate email
    valid, error = InputValidator.validate_email(email)
    if not valid:
        audit_logger.log_failed_auth(email, 'invalid_email', ip_address)
        return jsonify({'error': error}), 400
    
    db = get_db()
    user = db.users.find_one({'email': email})
    
    if not user:
        audit_logger.log_failed_auth(email, 'user_not_found', ip_address)
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Verify password
    if not security_manager.verify_password(password, user['password']):
        audit_logger.log_failed_auth(email, 'invalid_password', ip_address)
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate JWT token
    user_id = str(user['_id'])
    token = security_manager.generate_token(user_id, email)
    
    audit_logger.log_login(email, True, ip_address)
    
    # Return user data and token
    user_data = {
        '_id': user_id,
        'name': user.get('name'),
        'email': user['email'],
        'age': user.get('age'),
        'goal': user.get('goal', '')
    }
    
    return jsonify({
        'message': 'Login successful',
        'user': user_data,
        'token': token
    }), 200


@auth_bp.route('/user/<email>', methods=['GET'])
def get_user(email):
    """Get user profile by email"""
    import urllib.parse
    email = urllib.parse.unquote(email)
    
    db = get_db()
    user = db.users.find_one({'email': email})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user_data = {
        '_id': str(user['_id']),
        'name': user.get('name'),
        'email': user['email'],
        'age': user.get('age'),
        'goal': user.get('goal', '')
    }
    
    return jsonify(user_data), 200


@auth_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    """Verify email with token"""
    from backend.email_service import EmailTokenManager
    
    db = get_db()
    token_manager = EmailTokenManager(db)
    
    success, result = token_manager.verify_token(token)
    
    if success:
        audit_logger.log_info(f"Email verified: {result}")
        return jsonify({
            'message': 'Email verified successfully',
            'email': result
        }), 200
    else:
        return jsonify({'error': result}), 400


@auth_bp.route('/forgot-password', methods=['POST'])
@rate_limit("3 per hour")
def forgot_password():
    """Request password reset"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    db = get_db()
    user = db.users.find_one({'email': email})
    
    # Always return success to prevent email enumeration
    if user:
        token_manager = EmailTokenManager(db)
        token = token_manager.create_reset_token(email)
        
        try:
            email_service.send_password_reset_email(
                email, 
                user.get('name', 'User'),
                token
            )
        except Exception:
            pass  # Don't reveal errors
    
    return jsonify({
        'message': 'If the email exists, a password reset link has been sent'
    }), 200


@auth_bp.route('/reset-password', methods=['POST'])
@rate_limit("5 per hour")
def reset_password():
    """Reset password with token"""
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')
    
    if not token or not new_password:
        return jsonify({'error': 'Token and new password are required'}), 400
    
    # Validate new password
    valid, error = InputValidator.validate_password(new_password)
    if not valid:
        return jsonify({'error': error}), 400
    
    db = get_db()
    token_manager = EmailTokenManager(db)
    
    success, result = token_manager.verify_reset_token(token, new_password)
    
    if success:
        audit_logger.log_info(f"Password reset for: {result}")
        return jsonify({
            'message': 'Password reset successfully'
        }), 200
    else:
        return jsonify({'error': result}), 400


@auth_bp.route('/refresh-token', methods=['POST'])
@token_required
def refresh_token():
    """Refresh JWT token"""
    current_user = g.current_user
    
    new_token = security_manager.generate_token(
        current_user['user_id'],
        current_user['email']
    )
    
    return jsonify({
        'token': new_token
    }), 200
