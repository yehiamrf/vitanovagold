"""
Simple CSV-Based Authentication for VitaNova
=============================================
Uses Google Cloud Storage for persistent data storage
"""

from flask import Blueprint, request, jsonify, session
from datetime import datetime
import csv
import os
import io
from google.cloud import storage

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# GCS Configuration
BUCKET_NAME = 'vitanovamvp'
CSV_BLOB_PATH = 'gold_mvp_v3 Google/backend/Registered_Accounts.csv'

# Local fallback for development
LOCAL_CSV_FILE = os.path.join(os.path.dirname(__file__), 'Registered_Accounts.csv')

def get_storage_client():
        """Get GCS client"""
        try:
                    return storage.Client()
except Exception as e:
        print(f"Could not create GCS client: {e}")
        return None

def read_accounts_from_gcs():
        """Read accounts from GCS bucket"""
        accounts = []
        try:
                    client = get_storage_client()
                    if client:
                                    bucket = client.bucket(BUCKET_NAME)
                                    blob = bucket.blob(CSV_BLOB_PATH)
                                    if blob.exists():
                                                        content = blob.download_as_text()
                                                        reader = csv.DictReader(io.StringIO(content))
                                                        accounts = list(reader)
                                                        print(f"✅ Read {len(accounts)} accounts from GCS")
                    else:
                                        print(f"⚠️ CSV blob does not exist in GCS, will create on first registration")
        else:
                        # Fallback to local file
                        accounts = read_accounts_from_local()
except Exception as e:
        print(f"Error reading from GCS: {e}")
        accounts = read_accounts_from_local()
    return accounts

def read_accounts_from_local():
        """Fallback: Read accounts from local CSV"""
        accounts = []
        try:
                    if os.path.exists(LOCAL_CSV_FILE):
                                    with open(LOCAL_CSV_FILE, 'r', encoding='utf-8') as f:
                                                        reader = csv.DictReader(f)
                                                        accounts = list(reader)
                                                        print(f"📁 Read {len(accounts)} accounts from local file")
        except Exception as e:
                    print(f"Error reading local CSV: {e}")
                return accounts

def save_account_to_gcs(username, email, password, last_name, phone, customer_id):
        """Save account to GCS bucket"""
    try:
                client = get_storage_client()
                if client:
                                bucket = client.bucket(BUCKET_NAME)
                                blob = bucket.blob(CSV_BLOB_PATH)

            # Read existing content
                    existing_content = ""
            accounts = []
            if blob.exists():
                                existing_content = blob.download_as_text()
                                reader = csv.DictReader(io.StringIO(existing_content))
                                accounts = list(reader)

            # Add new account
            new_account = {
                                'username': username,
                                'email': email,
                                'password': password,
                                'last_name': last_name or '',
                                'phone': phone or '',
                                'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'customer_id': customer_id
            }
            accounts.append(new_account)

            # Write back to GCS
            output = io.StringIO()
            fieldnames = ['username', 'email', 'password', 'last_name', 'phone', 'registered_at', 'customer_id']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for account in accounts:
                                writer.writerow(account)

            blob.upload_from_string(output.getvalue(), content_type='text/csv')
            print(f"✅ Saved account for {email} to GCS bucket")
            return True
else:
            # Fallback to local
                return save_account_to_local(username, email, password, last_name, phone, customer_id)
except Exception as e:
        print(f"Error saving to GCS: {e}")
        return save_account_to_local(username, email, password, last_name, phone, customer_id)

def save_account_to_local(username, email, password, last_name, phone, customer_id):
        """Fallback: Save account to local CSV"""
    try:
                file_exists = os.path.exists(LOCAL_CSV_FILE)
        with open(LOCAL_CSV_FILE, 'a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        if not file_exists:
                                            writer.writerow(['username', 'email', 'password', 'last_name', 'phone', 'registered_at', 'customer_id'])
                                        writer.writerow([
                                                            username,
                                                            email,
                                                            password,
                                                            last_name or '',
                                                            phone or '',
                                                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                            customer_id
                                        ])
        print(f"📁 Saved account for {email} to local file")
        return True
except Exception as e:
        print(f"Error saving to local CSV: {e}")
        return False

def read_accounts():
        """Read all accounts - tries GCS first, falls back to local"""
    return read_accounts_from_gcs()

def get_user_by_email(email):
        """Get user data from CSV by email"""
    accounts = read_accounts()
    for account in accounts:
                if account['email'] == email:
                                return account
                        return None

def save_account(username, email, password, last_name, phone, customer_id):
        """Save account - tries GCS first, falls back to local"""
    return save_account_to_gcs(username, email, password, last_name, phone, customer_id)

def generate_customer_id():
        """Generate unique customer ID"""
    import random
    return str(random.randint(1000000000, 9999999999))

@auth_bp.route('/register', methods=['POST'])
def register():
        """Register new user"""
    try:
                data = request.get_json()

        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        last_name = data.get('lastName', '').strip()
        phone = data.get('phone', '').strip()

        # Validation
        if not username or not email or not password:
                        return jsonify({'success': False, 'message': 'الرجاء ملء جميع الحقول المطلوبة'}), 400

        # Check if email exists
        if get_user_by_email(email):
                        return jsonify({'success': False, 'message': 'البريد الإلكتروني مسجل بالفعل'}), 400

        # Generate customer ID
        customer_id = generate_customer_id()

        # Save account
        if save_account(username, email, password, last_name, phone, customer_id):
                        return jsonify({
                            'success': True,
                            'message': 'تم إنشاء الحساب بنجاح',
                            'customer_id': customer_id
        })
else:
            return jsonify({'success': False, 'message': 'حدث خطأ أثناء إنشاء الحساب'}), 500

except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء إنشاء الحساب'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
        """Login user"""
    try:
                data = request.get_json()

        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
                        return jsonify({'success': False, 'message': 'الرجاء إدخال البريد الإلكتروني وكلمة المرور'}), 400

        user = get_user_by_email(email)

        if not user:
                        return jsonify({'success': False, 'message': 'البريد الإلكتروني أو كلمة المرور غير صحيحة'}), 401

        if user['password'] != password:
                        return jsonify({'success': False, 'message': 'البريد الإلكتروني أو كلمة المرور غير صحيحة'}), 401

        # Set session
        session['user_email'] = email
        session['customer_id'] = user.get('customer_id', '')

        return jsonify({
                        'success': True,
                        'message': 'تم تسجيل الدخول بنجاح',
                        'user': {
                                            'username': user['username'],
                                            'email': user['email'],
                                            'customer_id': user.get('customer_id', ''),
                                            'last_name': user.get('last_name', ''),
                                            'phone': user.get('phone', '')
                        }
        })

except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء تسجيل الدخول'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
        """Logout user"""
    session.clear()
    return jsonify({'success': True, 'message': 'تم تسجيل الخروج بنجاح'})

@auth_bp.route('/user', methods=['GET'])
def get_current_user():
        """Get current logged in user"""
    email = session.get('user_email')
    if not email:
                return jsonify({'success': False, 'message': 'غير مسجل الدخول'}), 401

    user = get_user_by_email(email)
    if not user:
                session.clear()
        return jsonify({'success': False, 'message': 'المستخدم غير موجود'}), 404

    return jsonify({
                'success': True,
                'user': {
                                'username': user['username'],
                                'email': user['email'],
                                'customer_id': user.get('customer_id', ''),
                                'last_name': user.get('last_name', ''),
                                'phone': user.get('phone', '')
                }
    })

@auth_bp.route('/check-email', methods=['POST'])
def check_email():
        """Check if email exists"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()

    if get_user_by_email(email):
                return jsonify({'exists': True})
    return jsonify({'exists': False})
