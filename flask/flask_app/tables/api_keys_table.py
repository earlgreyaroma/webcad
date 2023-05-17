from .. import db
from flask_login import UserMixin
from datetime import datetime

# Access User PostgreSQL Table
class API_Keys(db.Model, UserMixin):
    __tablename__ = 'api_keys'
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    access_key = db.Column(db.String(255))
    secret_key = db.Column(db.String(255))