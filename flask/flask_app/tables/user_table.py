from .. import db
from flask_login import UserMixin
from datetime import datetime

# Access User PostgreSQL Table
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(255), nullable=False, unique=True)
    interactions = db.relationship('Interactions', backref='user')