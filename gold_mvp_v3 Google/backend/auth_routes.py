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
            writer.writerow(['username', 'email', 'password', 'last_name', 'phone', 'registered_at', 'customer_id'])
        print(f"✅ Created CSV: {CSV_FILE}")
    else:
        # Check if customer_id column exists, if not, add it
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header and 'customer_id' not in header:
                # Need to add customer_id column
                rows = [row for row in reader]
                
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'customer_id' not in content.split('\n')[0]:
                # Rewrite with customer_id column
                lines = content.split('\n')
                if lines[0]:
                    lines[0] = lines[0].rstrip() + ',customer_id'
                for i in range(1, len(lines)):
                    if lines[i].strip():
                        lines[i] = lines[i].rstrip() + f',{generate_customer_id()}'
                with open(CSV_FILE, 'w', encoding='utf-8') as fw:
                    fw.write('\n'.join(lines))
                print(f"✅ Added customer_id column to CSV")

init_csv()


def generate_customer_id():
    """Generate a unique 10-digit customer ID"""
    import random
    # Read existing customer IDs to avoid duplicates
    existing_ids = set()
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'customer_id' in row and row['customer_id']:
                    existing_ids.add(row['customer_id'])
    except:
        pass
    
    # Generate unique ID
    while True:
        new_id = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        if new_id not in existing_ids:
            return new_id


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


def get_user_by_email(email):
    """Get user data from CSV by email"""
    accounts = read_accounts()
    for account in accounts:
        if account['email'] == email:
            return account
    return None


def save_account(username, email, password, last_name, phone, customer_id):
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
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                customer_id
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
        
        # Generate unique customer ID
        customer_id = generate_customer_id()
        
        # Save to CSV
        if save_account(username, email, password, last_name, phone, customer_id):
            print(f"✅ User registered: {username} ({email}) - Customer ID: {customer_id}")
            return jsonify({
                'success': True,
                'message': 'تم إنشاء الحساب بنجاح',
                'user': {
                    'username': username,
                    'email': email,
                    'customer_id': customer_id
                }
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
                # Login successful - store in session
                customer_id = account.get('customer_id', '')
                
                session['user_email'] = email
                session['user_username'] = account['username']
                session['user_last_name'] = account.get('last_name', '')
                session['user_phone'] = account.get('phone', '')
                session['user_customer_id'] = customer_id
                
                print(f"✅ User logged in: {account['username']} - Customer ID: {customer_id}")
                
                return jsonify({
                    'success': True,
                    'message': 'تم تسجيل الدخول بنجاح',
                    'user': {
                        'username': account['username'],
                        'email': account['email'],
                        'last_name': account.get('last_name', ''),
                        'phone': account.get('phone', ''),
                        'customer_id': customer_id
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
    """Check if user is logged in and return full user data"""
    if 'user_email' in session:
        # Get fresh data from CSV
        user_data = get_user_by_email(session.get('user_email'))
        
        if user_data:
            return jsonify({
                'authenticated': True,
                'user': {
                    'email': user_data['email'],
                    'username': user_data['username'],
                    'last_name': user_data.get('last_name', ''),
                    'phone': user_data.get('phone', ''),
                    'customer_id': user_data.get('customer_id', '')
                }
            }), 200
        else:
            # User deleted from CSV
            session.clear()
            return jsonify({'authenticated': False}), 200
    
    return jsonify({'authenticated': False}), 200


def init_auth(app):
    """Initialize simple auth system"""
    app.config['SECRET_KEY'] = 'vitanova-secret-key-2024'
    app.register_blueprint(auth_bp)
    print("✅ Simple CSV authentication initialized")
