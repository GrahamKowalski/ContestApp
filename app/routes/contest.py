from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Contest, Entry, Vote
from app import db
import os
from werkzeug.utils import secure_filename
from config import Config
from datetime import datetime

bp = Blueprint('contest', __name__)

@bp.route('/contest/<int:contest_id>')
@login_required
def contest_detail(contest_id):
    contest = Contest.query.get_or_404(contest_id)
    now = datetime.utcnow()  # Get the current datetime
    return render_template('contest/detail.html', contest=contest, now=now)

@bp.route('/contest/<int:contest_id>/submit', methods=['GET', 'POST'])
@login_required
def submit_entry(contest_id):
    contest = Contest.query.get_or_404(contest_id)
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            upload_dir = Config.UPLOAD_FOLDER
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            entry = Entry(user_id=current_user.id, contest_id=contest.id, image_filename=filename)
            db.session.add(entry)
            db.session.commit()
            flash('Your entry has been submitted!')
            return redirect(url_for('contest.contest_detail', contest_id=contest.id))
    return render_template('contest/submit.html', contest=contest)

@bp.route('/contest/<int:contest_id>/vote', methods=['POST'])
@login_required
def vote(contest_id):
    entry_id = request.form['entry_id']
    entry = Entry.query.get_or_404(entry_id)
    if entry.contest_id != contest_id:
        flash('Invalid entry for this contest')
        return redirect(url_for('contest.contest_detail', contest_id=contest_id))
    existing_vote = Vote.query.filter_by(user_id=current_user.id, entry_id=entry_id).first()
    if existing_vote:
        flash('You have already voted for this entry')
    else:
        vote = Vote(user_id=current_user.id, entry_id=entry_id)
        db.session.add(vote)
        db.session.commit()
        flash('Your vote has been recorded!')
    return redirect(url_for('contest.contest_detail', contest_id=contest_id))