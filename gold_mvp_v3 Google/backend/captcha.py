"""
VitaNova hCaptcha Verification
==============================
hCaptcha integration for bot protection
"""

import requests
from config import HCAPTCHA_ENABLED, HCAPTCHA_SECRET_KEY

HCAPTCHA_VERIFY_URL = 'https://hcaptcha.com/siteverify'


def verify_hcaptcha(response_token, remote_ip=None):
    """
    Verify hCaptcha response token
    
    Args:
        response_token: The h-captcha-response token from the form
        remote_ip: Optional client IP address for additional verification
        
    Returns:
        tuple: (is_valid: bool, error_message or None)
    """
    # If hCaptcha is disabled, always return valid
    if not HCAPTCHA_ENABLED:
        print("⚠️ hCaptcha is disabled - allowing all requests")
        return True, None
    
    # Check if token is provided
    if not response_token:
        return False, 'يرجى إكمال التحقق من أنك لست روبوت'
    
    try:
        # Prepare verification data
        data = {
            'secret': HCAPTCHA_SECRET_KEY,
            'response': response_token
        }
        
        if remote_ip:
            data['remoteip'] = remote_ip
        
        # Make verification request
        response = requests.post(HCAPTCHA_VERIFY_URL, data=data, timeout=10)
        result = response.json()
        
        if result.get('success'):
            print("✅ hCaptcha verification successful")
            return True, None
        else:
            error_codes = result.get('error-codes', [])
            print(f"❌ hCaptcha verification failed: {error_codes}")
            
            # Map error codes to Arabic messages
            if 'missing-input-response' in error_codes:
                return False, 'يرجى إكمال التحقق من أنك لست روبوت'
            elif 'invalid-input-response' in error_codes:
                return False, 'فشل التحقق - يرجى المحاولة مرة أخرى'
            elif 'timeout-or-duplicate' in error_codes:
                return False, 'انتهت صلاحية التحقق - يرجى المحاولة مرة أخرى'
            else:
                return False, 'فشل التحقق - يرجى المحاولة مرة أخرى'
                
    except requests.Timeout:
        print("❌ hCaptcha verification timeout")
        return False, 'انتهت مهلة الاتصال - يرجى المحاولة مرة أخرى'
    except requests.RequestException as e:
        print(f"❌ hCaptcha verification error: {e}")
        return False, 'حدث خطأ في التحقق - يرجى المحاولة مرة أخرى'
    except Exception as e:
        print(f"❌ Unexpected hCaptcha error: {e}")
        return False, 'حدث خطأ غير متوقع'


def get_hcaptcha_script():
    """
    Get the hCaptcha script tag for HTML pages
    
    Returns:
        str: HTML script tag
    """
    return '<script src="https://js.hcaptcha.com/1/api.js" async defer></script>'


def get_hcaptcha_widget(site_key=None):
    """
    Get the hCaptcha widget HTML
    
    Args:
        site_key: Optional override for site key
        
    Returns:
        str: HTML div for hCaptcha widget
    """
    from config import HCAPTCHA_SITE_KEY
    key = site_key or HCAPTCHA_SITE_KEY
    return f'<div class="h-captcha" data-sitekey="{key}" data-theme="dark"></div>'
