from . import db
from flask_login import UserMixin
from sqlalchemy.ext.mutable import MutableList

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    
    completed_lessons = db.Column(MutableList.as_mutable(db.JSON), default=list)
    completed_challenges = db.Column(MutableList.as_mutable(db.JSON), default=list)
    
    role = db.Column(db.String(20), default='user')
    
    def has_role(self, role):
        return self.role == role
    
    def is_admin(self):
        return self.role == 'admin'