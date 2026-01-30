"""
Simple CSV-Based Authentication for VitaNova
============================================
No encryption, no email verification - just CSV storage
"""

from flask import Blueprint, request, jsonify, session
from datetime import datetime
import csv
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# CSV file path
CSV_FILE = os.path.join(os.path.dirname(__file__), 'Registered_Accounts.csv')

# Initialize CSV file
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'email', 'password', 'last_name', 'phone', 'registered_at'])
        print(f"✅ Created CSV: {CSV_FILE}")

init_csv()


def read_accounts():
    """Read all accounts from CSV"""
    accounts = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            accounts = list(reader)
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return accounts


def save_account(username, email, password, last_name, phone):
    """Save account to CSV"""
    try:
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                username,
                email,
                password,  # Plain text - no encryption
                last_name or '',
                phone or '',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ])
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user - save to CSV"""
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        last_name = data.get('last_name', '').strip()
        phone = data.get('phone', '').strip()
        accept_terms = data.get('accept_terms', False)
        
        # Validate
        if not username or len(username) < 3:
            return jsonify({'success': False, 'error': 'اسم المستخدم يجب أن يكون 3 أحرف على الأقل', 'field': 'username'}), 400
        
        if not email:
            return jsonify({'success': False, 'error': 'البريد الإلكتروني مطلوب', 'field': 'email'}), 400
        
        if len(password) < 8:
            return jsonify({'success': False, 'error': 'كلمة المرور يجب أن تكون 8 أحرف على الأقل', 'field': 'password'}), 400
        
        if password != confirm_password:
            return jsonify({'success': False, 'error': 'كلمة المرور غير متطابقة', 'field': 'confirm_password'}), 400
        
        if not accept_terms:
            return jsonify({'success': False, 'error': 'يجب الموافقة على الشروط والأحكام', 'field': 'accept_terms'}), 400
        
        # Check if email already exists
        accounts = read_accounts()
        for account in accounts:
            if account['email'] == email:
                return jsonify({'success': False, 'error': 'البريد الإلكتروني مسجل بالفعل', 'field': 'email'}), 409
            if account['username'] == username:
                return jsonify({'success': False, 'error': 'اسم المستخدم مستخدم بالفعل', 'field': 'username'}), 409
        
        # Save to CSV
        if save_account(username, email, password, last_name, phone):
            print(f"✅ User registered: {username} ({email})")
            return jsonify({
                'success': True,
                'message': 'تم إنشاء الحساب بنجاح',
                'user': {'username': username, 'email': email}
            }), 201
        else:
            return jsonify({'success': False, 'error': 'فشل حفظ البيانات'}), 500
        
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return jsonify({'success': False, 'error': 'حدث خطأ أثناء التسجيل'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user - check against CSV (email + password only)"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email:
            return jsonify({'success': False, 'error': 'البريد الإلكتروني مطلوب'}), 400
        
        if not password:
            return jsonify({'success': False, 'error': 'كلمة المرور مطلوبة'}), 400
        
        # Check CSV
        accounts = read_accounts()
        for account in accounts:
            if account['email'] == email and account['password'] == password:
                # Login successful
                session['user_email'] = email
                session['user_username'] = account['username']
                
                print(f"✅ User logged in: {account['username']}")
                
                return jsonify({
                    'success': True,
                    'message': 'تم تسجيل الدخول بنجاح',
                    'user': {
                        'username': account['username'],
                        'email': account['email'],
                        'last_name': account.get('last_name', ''),
                        'phone': account.get('phone', '')
                    }
                }), 200
        
        # Login failed
        return jsonify({'success': False, 'error': 'البريد الإلكتروني أو كلمة المرور غير صحيحة'}), 401
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        return jsonify({'success': False, 'error': 'حدث خطأ أثناء تسجيل الدخول'}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'success': True, 'message': 'تم تسجيل الخروج بنجاح'}), 200


@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """Check if user is logged in"""
    if 'user_email' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'email': session.get('user_email'),
                'username': session.get('user_username')
            }
        }), 200
    return jsonify({'authenticated': False}), 200


def init_auth(app):
    """Initialize simple auth system"""
    app.config['SECRET_KEY'] = 'vitanova-secret-key-2024'
    app.register_blueprint(auth_bp)
    print("✅ Simple CSV authentication initialized")
