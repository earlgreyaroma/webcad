from .. import db 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Access Admin PostgreSQL Table
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    admin_check = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255))
    actions = db.relationship('Actions', backref='user')
    api_keys = db.relationship('API_Keys', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='scrypt')
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)