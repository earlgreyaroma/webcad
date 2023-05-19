from .. import db
from datetime import datetime

# Access User PostgreSQL Table
class API_Keys(db.Model):
    __tablename__ = 'api_keys'
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    access_key = db.Column(db.String(255))
    secret_key = db.Column(db.String(255))