from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import User, ExamAttempt
from extensions import db
from sqlalchemy import desc

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get user's exam history
    exam_history = ExamAttempt.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).order_by(desc(ExamAttempt.end_time)).limit(5).all()
    
    # Get user's best score
    best_score = current_user.get_best_score()
    level = current_user.get_level()
    
    return render_template('dashboard.html',
                         exam_history=exam_history,
                         best_score=best_score,
                         level=level)

@main_bp.route('/leaderboard')
@login_required
def leaderboard():
    # Only admin can view leaderboard
    if not current_user.is_admin:
        flash('Liderlik tablosuna erişim yetkiniz yok.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get top users by best score
    users_data = []
    users = User.query.all()
    
    for user in users:
        best_score = user.get_best_score()
        if best_score > 0:
            users_data.append({
                'user': user,
                'score': best_score,
                'level': user.get_level()
            })
    
    # Sort by score
    users_data.sort(key=lambda x: x['score'], reverse=True)
    
    return render_template('leaderboard.html', leaderboard=users_data)

from flask import redirect, url_for
