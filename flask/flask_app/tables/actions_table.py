from .. import db
from datetime import datetime

# Access User Interactions PostgreSQL Table
class Actions(db.Model):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))