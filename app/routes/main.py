from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Contest
from datetime import datetime


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/home')
@login_required
def home():
    active_contests = Contest.query.filter(Contest.end_voting_date > datetime.utcnow()).all()
    past_contests = Contest.query.filter(Contest.end_voting_date <= datetime.utcnow()).all()
    return render_template('home.html', active_contests=active_contests, past_contests=past_contests)