"""
VitaNova Password Validation
============================
Password strength validation with Arabic support
"""

import re
from config import (
    PASSWORD_MIN_LENGTH,
    PASSWORD_REQUIRE_UPPERCASE,
    PASSWORD_REQUIRE_LOWERCASE,
    PASSWORD_REQUIRE_NUMBER,
    PASSWORD_REQUIRE_SPECIAL
)


def validate_password(password):
    """
    Validate password against security requirements
    
    Args:
        password: The password to validate
        
    Returns:
        tuple: (is_valid: bool, errors: list of error messages in Arabic)
    """
    errors = []
    
    # Check minimum length
    if len(password) < PASSWORD_MIN_LENGTH:
        errors.append(f'كلمة المرور يجب أن تكون {PASSWORD_MIN_LENGTH} أحرف على الأقل')
    
    # Check for uppercase letter
    if PASSWORD_REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
        errors.append('كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل')
    
    # Check for lowercase letter
    if PASSWORD_REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
        errors.append('كلمة المرور يجب أن تحتوي على حرف صغير واحد على الأقل')
    
    # Check for number
    if PASSWORD_REQUIRE_NUMBER and not re.search(r'\d', password):
        errors.append('كلمة المرور يجب أن تحتوي على رقم واحد على الأقل')
    
    # Check for special character (optional)
    if PASSWORD_REQUIRE_SPECIAL and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append('كلمة المرور يجب أن تحتوي على رمز خاص واحد على الأقل')
    
    is_valid = len(errors) == 0
    return is_valid, errors


def validate_username(username):
    """
    Validate username
    
    Args:
        username: The username to validate
        
    Returns:
        tuple: (is_valid: bool, error message or None)
    """
    # Check minimum length
    if len(username) < 3:
        return False, 'اسم المستخدم يجب أن يكون 3 أحرف على الأقل'
    
    # Check maximum length
    if len(username) > 50:
        return False, 'اسم المستخدم يجب أن يكون أقل من 50 حرف'
    
    # Allow Arabic, English, numbers, underscore, and dash
    # Arabic Unicode range: \u0600-\u06FF
    pattern = r'^[\u0600-\u06FFa-zA-Z0-9_-]+$'
    if not re.match(pattern, username):
        return False, 'اسم المستخدم يمكن أن يحتوي على حروف عربية أو إنجليزية وأرقام وشرطات فقط'
    
    return True, None


def validate_email(email):
    """
    Validate email format
    
    Args:
        email: The email to validate
        
    Returns:
        tuple: (is_valid: bool, error message or None)
    """
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not email:
        return False, 'البريد الإلكتروني مطلوب'
    
    if not re.match(pattern, email):
        return False, 'صيغة البريد الإلكتروني غير صحيحة'
    
    return True, None


def get_password_strength(password):
    """
    Calculate password strength score
    
    Args:
        password: The password to evaluate
        
    Returns:
        dict: {
            'score': int (0-5),
            'strength': str ('ضعيفة'/'متوسطة'/'قوية'/'قوية جداً'),
            'color': str (CSS color)
        }
    """
    score = 0
    
    # Length score
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    
    # Character variety
    if re.search(r'[a-z]', password):
        score += 0.5
    if re.search(r'[A-Z]', password):
        score += 0.5
    if re.search(r'\d', password):
        score += 0.5
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 0.5
    
    # Round score
    score = int(score)
    
    # Determine strength
    if score <= 1:
        return {'score': score, 'strength': 'ضعيفة', 'color': '#CD7F32'}  # Bronze
    elif score <= 2:
        return {'score': score, 'strength': 'متوسطة', 'color': '#F4B942'}  # Warn
    elif score <= 3:
        return {'score': score, 'strength': 'قوية', 'color': '#B8860B'}  # Gold
    else:
        return {'score': score, 'strength': 'قوية جداً', 'color': '#FFD700'}  # Bright gold
