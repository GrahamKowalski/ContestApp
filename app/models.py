# app/models.py
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from sqlalchemy import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    entries = db.relationship('Entry', backref='user', lazy='dynamic')  # Add this line

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Contest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_submission_date = db.Column(db.DateTime, nullable=False)
    end_voting_date = db.Column(db.DateTime, nullable=False)
    theme = db.Column(db.String(100))
    entries = db.relationship('Entry', backref='contest', lazy='dynamic')

    def sorted_entries(self):
        return self.entries.join(Vote).group_by(Entry.id).order_by(func.count(Vote.id).desc()).all()

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.id'), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    votes = db.relationship('Vote', backref='entry', lazy='dynamic')

    def vote_count(self):
        return self.votes.count()

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)