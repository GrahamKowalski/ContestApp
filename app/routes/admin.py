from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Contest, Entry
from app import db
from datetime import datetime

bp = Blueprint('admin', __name__)

@bp.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.home'))
    active_contests = Contest.query.filter(Contest.end_voting_date > datetime.utcnow()).all()
    past_contests = Contest.query.filter(Contest.end_voting_date <= datetime.utcnow()).all()
    return render_template('admin/dashboard.html', active_contests=active_contests, past_contests=past_contests)

@bp.route('/admin/create_contest', methods=['GET', 'POST'])
@login_required
def create_contest():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        contest = Contest(
            name=request.form['name'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            end_submission_date=datetime.strptime(request.form['end_submission_date'], '%Y-%m-%d'),
            end_voting_date=datetime.strptime(request.form['end_voting_date'], '%Y-%m-%d'),
            theme=request.form['theme']
        )
        db.session.add(contest)
        db.session.commit()
        flash('Contest created successfully!')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/create_contest.html')

@bp.route('/admin/contest/<int:contest_id>', methods=['GET', 'POST'])
@login_required
def manage_contest(contest_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.home'))
    
    contest = Contest.query.get_or_404(contest_id)
    
    if request.method == 'POST':
        contest.name = request.form['name']
        contest.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        contest.end_submission_date = datetime.strptime(request.form['end_submission_date'], '%Y-%m-%d')
        contest.end_voting_date = datetime.strptime(request.form['end_voting_date'], '%Y-%m-%d')
        contest.theme = request.form['theme']
        
        db.session.commit()
        flash('Contest updated successfully!')
        return redirect(url_for('admin.manage_contest', contest_id=contest.id))
    
    entries = Entry.query.filter_by(contest_id=contest.id).all()
    now = datetime.utcnow()  # Add this line to get the current time
    return render_template('admin/manage_contest.html', contest=contest, entries=entries, now=now)  # Pass 'now' to the template


@bp.route('/admin/contest/<int:contest_id>/action', methods=['POST'])
@login_required
def contest_action(contest_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('main.home'))
    
    contest = Contest.query.get_or_404(contest_id)
    action = request.form.get('action')

    if action == 'start_voting':
        contest.end_submission_date = datetime.utcnow()
        flash('Submission period closed and voting period started.')
    elif action == 'end_voting':
        contest.end_voting_date = datetime.utcnow()
        flash('Voting period ended and contest moved to past contests.')
    
    db.session.commit()
    return redirect(url_for('admin.manage_contest', contest_id=contest.id))