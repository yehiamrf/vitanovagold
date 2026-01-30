"""
VitaNova Authentication Configuration
=====================================
Central configuration for all authentication settings
"""

import os
import secrets

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============== SECRET KEY ==============
# Generate a random secret key for production
# In production, set this via environment variable
SECRET_KEY = os.environ.get('VITANOVA_SECRET_KEY') or secrets.token_hex(32)

# ============== DATABASE ==============
DATABASE_PATH = os.path.join(BASE_DIR, 'vitanova.db')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ============== BCRYPT ==============
BCRYPT_LOG_ROUNDS = 12  # Higher = more secure but slower

# ============== SESSION ==============
SESSION_COOKIE_SECURE = False  # Set True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
REMEMBER_COOKIE_DURATION = 30  # Days

# ============== hCAPTCHA ==============
# Get free keys from: https://www.hcaptcha.com/
# These are test keys - replace with your own in production
# DISABLED FOR PROTOTYPE - Set to True when you have real API keys
HCAPTCHA_ENABLED = False
HCAPTCHA_SITE_KEY = os.environ.get('HCAPTCHA_SITE_KEY') or '10000000-ffff-ffff-ffff-000000000001'  # Test key
HCAPTCHA_SECRET_KEY = os.environ.get('HCAPTCHA_SECRET_KEY') or '0x0000000000000000000000000000000000000000'  # Test key

# ============== TOKEN EXPIRATION ==============
EMAIL_VERIFICATION_EXPIRATION = 3600  # 1 hour in seconds
PASSWORD_RESET_EXPIRATION = 1800  # 30 minutes in seconds

# ============== CSV PATHS ==============
EMAIL_PENDING_CSV = os.path.join(BASE_DIR, 'emails_pending_verification.csv')
PASSWORD_RESET_CSV = os.path.join(BASE_DIR, 'password_reset_requests.csv')

# ============== PASSWORD REQUIREMENTS ==============
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_NUMBER = True
PASSWORD_REQUIRE_SPECIAL = False  # Optional for MVP

# ============== RATE LIMITING ==============
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_MINUTES = 15
