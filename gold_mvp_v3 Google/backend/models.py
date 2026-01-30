"""
VitaNova Database Models
========================
User model with password hashing and authentication utilities
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

# Initialize extensions (will be initialized with app later)
db = SQLAlchemy()
bcrypt = Bcrypt()


class User(UserMixin, db.Model):
    """
    User model for VitaNova authentication
    
    Attributes:
        id: Primary key
        username: Unique username (Arabic supported)
        email: Unique email address
        password_hash: Bcrypt hashed password
        is_verified: Email verification status
        is_active: Account active status
        created_at: Account creation timestamp
        last_login: Last successful login timestamp
        failed_login_attempts: Counter for rate limiting
        locked_until: Lockout timestamp if too many failed attempts
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Account status
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)
    
    # Security
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    
    # Profile (optional)
    full_name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    customer_id = db.Column(db.String(10), unique=True, nullable=True, index=True)
    
    def __init__(self, username, email, password, full_name=None, phone=None):
        """Create a new user with hashed password"""
        self.username = username
        self.email = email.lower()  # Normalize email
        self.set_password(password)
        self.full_name = full_name
        self.phone = phone
        self.customer_id = self.generate_customer_id()
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    @staticmethod
    def generate_customer_id():
        """Generate a unique 10-digit customer ID"""
        import random
        while True:
            customer_id = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            # Check if this ID already exists
            if not User.query.filter_by(customer_id=customer_id).first():
                return customer_id
    
    def check_password(self, password):
        """Verify password against hash"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def is_locked(self):
        """Check if account is currently locked"""
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until
    
    def record_failed_login(self, max_attempts=5, lockout_minutes=15):
        """Record a failed login attempt"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= max_attempts:
            from datetime import timedelta
            self.locked_until = datetime.utcnow() + timedelta(minutes=lockout_minutes)
        db.session.commit()
    
    def record_successful_login(self):
        """Record a successful login"""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def verify_email(self):
        """Mark email as verified"""
        self.is_verified = True
        self.verified_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert user to dictionary (safe for JSON)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'full_name': self.full_name,
            'phone': self.phone,
            'customer_id': self.customer_id
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class LoginLog(db.Model):
    """
    Log of login attempts for security auditing
    """
    __tablename__ = 'login_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    username_attempted = db.Column(db.String(50), nullable=False)
    success = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    failure_reason = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f'<LoginLog {self.username_attempted} - {"Success" if self.success else "Failed"}>'


def init_db(app):
    """Initialize the database with the Flask app"""
    db.init_app(app)
    bcrypt.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully")
