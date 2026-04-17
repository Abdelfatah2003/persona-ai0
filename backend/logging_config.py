"""
Logging Configuration and Utilities
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os

def setup_logging(app=None, log_level='INFO'):
    """
    Configure application logging with file and console handlers
    """
    # Create logs directory
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Clear existing handlers
    logger.handlers = []
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (with rotation)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'persona_ai.log'),
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Error file handler
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, 'persona_ai_errors.log'),
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    # Request logging handler
    request_handler = RotatingFileHandler(
        os.path.join(log_dir, 'requests.log'),
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    request_handler.setLevel(logging.INFO)
    request_handler.setFormatter(formatter)
    
    if app:
        # Log application startup
        logger.info("=" * 60)
        logger.info("PersonaAI Application Starting")
        logger.info(f"Environment: {app.config.get('ENV', 'development')}")
        logger.info(f"Debug Mode: {app.config.get('DEBUG', False)}")
        logger.info("=" * 60)
    
    return logger


class RequestLogger:
    """Middleware for logging HTTP requests"""
    
    def __init__(self, app=None):
        self.logger = logging.getLogger('request_logger')
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize request logging for Flask app"""
        import time
        from flask import request, g
        
        @app.before_request
        def log_request_info():
            g.start_time = time.time()
            self.logger.info(
                f"REQUEST: {request.method} {request.path} | "
                f"IP: {request.remote_addr} | "
                f"User-Agent: {request.user_agent.string[:50]}"
            )
        
        @app.after_request
        def log_response_info(response):
            duration = time.time() - g.get('start_time', time.time())
            self.logger.info(
                f"RESPONSE: {request.method} {request.path} | "
                f"Status: {response.status_code} | "
                f"Duration: {duration:.3f}s"
            )
            return response


class AuditLogger:
    """Logger for security and audit events"""
    
    def __init__(self):
        self.logger = logging.getLogger('audit_logger')
    
    def log_login(self, email, success, ip_address):
        """Log login attempt"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"LOGIN {status}: {email} from {ip_address}")
    
    def log_logout(self, email):
        """Log logout"""
        self.logger.info(f"LOGOUT: {email}")
    
    def log_registration(self, email, success):
        """Log registration"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"REGISTRATION {status}: {email}")
    
    def log_failed_auth(self, email, reason, ip_address):
        """Log failed authentication"""
        self.logger.warning(
            f"AUTH FAILED: {email} | Reason: {reason} | IP: {ip_address}"
        )
    
    def log_quiz_completed(self, email, traits):
        """Log quiz completion"""
        self.logger.info(
            f"QUIZ COMPLETED: {email} | Traits: {traits}"
        )
    
    def log_data_access(self, user_id, resource, action):
        """Log data access"""
        self.logger.info(
            f"DATA ACCESS: User {user_id} | {action} {resource}"
        )


# Global instances
audit_logger = AuditLogger()


def log_info(message, **kwargs):
    """Log info message"""
    logging.getLogger().info(message, extra=kwargs)


def log_error(message, **kwargs):
    """Log error message"""
    logging.getLogger().error(message, extra=kwargs)


def log_warning(message, **kwargs):
    """Log warning message"""
    logging.getLogger().warning(message, extra=kwargs)


def log_debug(message, **kwargs):
    """Log debug message"""
    logging.getLogger().debug(message, extra=kwargs)
