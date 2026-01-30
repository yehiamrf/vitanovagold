"""
VitaNova CSV Email Logger
=========================
Log emails to CSV for later batch sending/verification
"""

import csv
import os
from datetime import datetime
from config import EMAIL_PENDING_CSV, PASSWORD_RESET_CSV


def ensure_csv_exists(filepath, headers):
    """Create CSV file with headers if it doesn't exist"""
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)


def log_verification_email(email, username, token):
    """
    Log a verification email request to CSV
    
    Args:
        email: User's email address
        username: User's username
        token: Verification token
        
    Returns:
        bool: True if logged successfully
    """
    headers = ['email', 'username', 'token', 'timestamp', 'status', 'sent_at', 'verified_at']
    ensure_csv_exists(EMAIL_PENDING_CSV, headers)
    
    try:
        with open(EMAIL_PENDING_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                email,
                username,
                token,
                datetime.now().isoformat(),
                'pending',
                '',  # sent_at (empty until sent)
                ''   # verified_at (empty until verified)
            ])
        print(f"📧 Verification email logged for: {email}")
        return True
    except Exception as e:
        print(f"❌ Error logging verification email: {e}")
        return False


def log_password_reset(email, token):
    """
    Log a password reset request to CSV
    
    Args:
        email: User's email address
        token: Reset token
        
    Returns:
        bool: True if logged successfully
    """
    headers = ['email', 'token', 'timestamp', 'status', 'sent_at', 'used_at']
    ensure_csv_exists(PASSWORD_RESET_CSV, headers)
    
    try:
        with open(PASSWORD_RESET_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                email,
                token,
                datetime.now().isoformat(),
                'pending',
                '',  # sent_at
                ''   # used_at
            ])
        print(f"🔑 Password reset logged for: {email}")
        return True
    except Exception as e:
        print(f"❌ Error logging password reset: {e}")
        return False


def update_verification_status(email, status, column='status'):
    """
    Update the status of a verification email in CSV
    
    Args:
        email: User's email address
        status: New status ('sent', 'verified', 'expired', 'failed')
        column: Which column to update
    """
    if not os.path.exists(EMAIL_PENDING_CSV):
        return False
    
    try:
        rows = []
        headers = None
        
        with open(EMAIL_PENDING_CSV, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            
            for row in reader:
                if row[0] == email:  # email column
                    if column == 'status':
                        row[4] = status
                    elif column == 'sent_at':
                        row[5] = datetime.now().isoformat()
                    elif column == 'verified_at':
                        row[6] = datetime.now().isoformat()
                        row[4] = 'verified'
                rows.append(row)
        
        with open(EMAIL_PENDING_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        
        return True
    except Exception as e:
        print(f"❌ Error updating verification status: {e}")
        return False


def get_pending_verification_emails():
    """
    Get all pending verification emails
    
    Returns:
        list: List of dicts with pending email info
    """
    if not os.path.exists(EMAIL_PENDING_CSV):
        return []
    
    pending = []
    try:
        with open(EMAIL_PENDING_CSV, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('status') == 'pending':
                    pending.append(row)
    except Exception as e:
        print(f"❌ Error reading pending emails: {e}")
    
    return pending


def get_pending_password_resets():
    """
    Get all pending password reset requests
    
    Returns:
        list: List of dicts with pending reset info
    """
    if not os.path.exists(PASSWORD_RESET_CSV):
        return []
    
    pending = []
    try:
        with open(PASSWORD_RESET_CSV, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('status') == 'pending':
                    pending.append(row)
    except Exception as e:
        print(f"❌ Error reading pending resets: {e}")
    
    return pending


def mark_reset_as_used(email):
    """Mark a password reset as used"""
    if not os.path.exists(PASSWORD_RESET_CSV):
        return False
    
    try:
        rows = []
        headers = None
        
        with open(PASSWORD_RESET_CSV, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            
            for row in reader:
                if row[0] == email and row[3] == 'pending':
                    row[3] = 'used'
                    row[5] = datetime.now().isoformat()
                rows.append(row)
        
        with open(PASSWORD_RESET_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        
        return True
    except Exception as e:
        print(f"❌ Error marking reset as used: {e}")
        return False
