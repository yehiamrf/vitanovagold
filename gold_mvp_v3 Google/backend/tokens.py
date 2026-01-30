"""
VitaNova Token Utilities
========================
Secure token generation and verification using itsdangerous
"""

from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from config import SECRET_KEY, EMAIL_VERIFICATION_EXPIRATION, PASSWORD_RESET_EXPIRATION

# Token serializer
serializer = URLSafeTimedSerializer(SECRET_KEY)


def generate_email_verification_token(email):
    """
    Generate a secure token for email verification
    
    Args:
        email: User's email address
        
    Returns:
        str: URL-safe token
    """
    return serializer.dumps(email, salt='email-verification')


def verify_email_token(token, expiration=EMAIL_VERIFICATION_EXPIRATION):
    """
    Verify an email verification token
    
    Args:
        token: The token to verify
        expiration: Max age in seconds (default: 1 hour)
        
    Returns:
        str: Email address if valid
        None: If token is invalid or expired
    """
    try:
        email = serializer.loads(
            token,
            salt='email-verification',
            max_age=expiration
        )
        return email
    except (SignatureExpired, BadSignature):
        return None


def generate_password_reset_token(email):
    """
    Generate a secure token for password reset
    
    Args:
        email: User's email address
        
    Returns:
        str: URL-safe token
    """
    return serializer.dumps(email, salt='password-reset')


def verify_password_reset_token(token, expiration=PASSWORD_RESET_EXPIRATION):
    """
    Verify a password reset token
    
    Args:
        token: The token to verify
        expiration: Max age in seconds (default: 30 minutes)
        
    Returns:
        str: Email address if valid
        None: If token is invalid or expired
    """
    try:
        email = serializer.loads(
            token,
            salt='password-reset',
            max_age=expiration
        )
        return email
    except SignatureExpired:
        return None
    except BadSignature:
        return None


def generate_remember_me_token(user_id, password_hash):
    """
    Generate a secure "remember me" token
    
    Uses both user_id and password_hash so token becomes invalid
    when password changes
    
    Args:
        user_id: User's ID
        password_hash: Current password hash
        
    Returns:
        str: Secure remember token
    """
    data = f"{user_id}:{password_hash[:20]}"  # Use partial hash
    return serializer.dumps(data, salt='remember-me')


def verify_remember_me_token(token, max_age_days=30):
    """
    Verify a "remember me" token
    
    Args:
        token: The remember token
        max_age_days: Maximum age in days
        
    Returns:
        tuple: (user_id, partial_hash) if valid
        None: If invalid or expired
    """
    try:
        max_age_seconds = max_age_days * 24 * 60 * 60
        data = serializer.loads(
            token,
            salt='remember-me',
            max_age=max_age_seconds
        )
        parts = data.split(':')
        if len(parts) == 2:
            return int(parts[0]), parts[1]
        return None
    except (SignatureExpired, BadSignature, ValueError):
        return None
