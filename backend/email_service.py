"""
Email Service for Verification and Password Reset
"""
import os
import secrets
from datetime import datetime, timedelta
from flask import current_app


class EmailService:
    """
    Email service for sending verification and password reset emails
    Note: This is a template implementation. In production, integrate with
    actual email service (SendGrid, AWS SES, Mailgun, etc.)
    """
    
    def __init__(self):
        self.from_email = os.environ.get('FROM_EMAIL', 'noreply@persona-ai.com')
        self.from_name = 'PersonaAI'
    
    def generate_verification_token(self):
        """Generate email verification token"""
        return secrets.token_urlsafe(48)
    
    def generate_reset_token(self):
        """Generate password reset token"""
        return secrets.token_urlsafe(32)
    
    def send_verification_email(self, email, user_name, token):
        """Send email verification email"""
        verification_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/verify-email/{token}"
        
        subject = "Verify Your Email - PersonaAI"
        body = f"""
        Hi {user_name},
        
        Thank you for registering with PersonaAI!
        
        Please verify your email address by clicking the link below:
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't create an account with PersonaAI, please ignore this email.
        
        Best regards,
        The PersonaAI Team
        """
        
        return self._send_email(email, subject, body)
    
    def send_password_reset_email(self, email, user_name, token):
        """Send password reset email"""
        reset_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/reset-password/{token}"
        
        subject = "Password Reset - PersonaAI"
        body = f"""
        Hi {user_name},
        
        We received a request to reset your password.
        
        Click the link below to reset your password:
        {reset_url}
        
        This link will expire in 1 hour.
        
        If you didn't request a password reset, please ignore this email and your password will remain unchanged.
        
        Best regards,
        The PersonaAI Team
        """
        
        return self._send_email(email, subject, body)
    
    def send_welcome_email(self, email, user_name):
        """Send welcome email after registration"""
        subject = "Welcome to PersonaAI!"
        body = f"""
        Welcome, {user_name}!
        
        Thank you for joining PersonaAI! We're excited to help you discover your personality and find the perfect career path.
        
        Here's what you can do next:
        1. Complete your personality quiz
        2. Explore your career recommendations
        3. Connect with like-minded people
        
        Good luck on your journey!
        
        Best regards,
        The PersonaAI Team
        """
        
        return self._send_email(email, subject, body)
    
    def send_quiz_completion_email(self, email, user_name, personality_type):
        """Send email when quiz is completed"""
        subject = "Your Personality Profile is Ready!"
        body = f"""
        Hi {user_name},
        
        Great news! Your personality analysis is complete.
        
        Your personality type: {personality_type}
        
        Log in to view your detailed results, career recommendations, and connect with similar people.
        
        Best regards,
        The PersonaAI Team
        """
        
        return self._send_email(email, subject, body)
    
    def _send_email(self, to_email, subject, body):
        """
        Send email (template method)
        In production, implement actual email sending here
        """
        # In production, integrate with email service:
        # - SendGrid
        # - AWS SES
        # - Mailgun
        # - SMTP server
        
        email_data = {
            'from': f"{self.from_name} <{self.from_email}>",
            'to': to_email,
            'subject': subject,
            'body': body
        }
        
        # Log email (for development)
        import logging
        logger = logging.getLogger()
        logger.info(f"EMAIL SENT: To: {to_email} | Subject: {subject}")
        
        # Return success (in production, return actual result)
        return {
            'success': True,
            'message': 'Email queued for sending',
            'email_id': secrets.token_hex(8)
        }


class EmailTokenManager:
    """Manage email verification and reset tokens"""
    
    def __init__(self, db):
        self.db = db
        self.verification_collection = db.email_verifications
        self.reset_collection = db.password_resets
        
        # Create indexes
        self.verification_collection.create_index('token', unique=True)
        self.verification_collection.create_index('email')
        self.reset_collection.create_index('token', unique=True)
        self.reset_collection.create_index('email')
    
    def create_verification_token(self, email, user_id):
        """Create email verification token"""
        service = EmailService()
        token = service.generate_verification_token()
        
        document = {
            'email': email,
            'user_id': str(user_id),
            'token': token,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(hours=24),
            'verified': False
        }
        
        self.verification_collection.insert_one(document)
        return token
    
    def verify_token(self, token):
        """Verify email verification token"""
        document = self.verification_collection.find_one({
            'token': token,
            'verified': False
        })
        
        if not document:
            return False, "Token not found"
        
        if document['expires_at'] < datetime.utcnow():
            return False, "Token expired"
        
        # Mark as verified
        self.verification_collection.update_one(
            {'token': token},
            {'$set': {'verified': True, 'verified_at': datetime.utcnow()}}
        )
        
        return True, document['email']
    
    def create_reset_token(self, email):
        """Create password reset token"""
        service = EmailService()
        token = service.generate_reset_token()
        
        # Delete any existing reset tokens for this email
        self.reset_collection.delete_many({'email': email})
        
        document = {
            'email': email,
            'token': token,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(hours=1),
            'used': False
        }
        
        self.reset_collection.insert_one(document)
        return token
    
    def verify_reset_token(self, token, new_password):
        """Verify password reset token and update password"""
        document = self.reset_collection.find_one({
            'token': token,
            'used': False
        })
        
        if not document:
            return False, "Token not found"
        
        if document['expires_at'] < datetime.utcnow():
            return False, "Token expired"
        
        # Update password
        from backend.security import security_manager
        hashed_password = security_manager.hash_password(new_password)
        
        self.db.users.update_one(
            {'email': document['email']},
            {'$set': {'password': hashed_password, 'updated_at': datetime.utcnow()}}
        )
        
        # Mark token as used
        self.reset_collection.update_one(
            {'token': token},
            {'$set': {'used': True, 'used_at': datetime.utcnow()}}
        )
        
        return True, document['email']


# Global instance
email_service = EmailService()
