from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Question, User, ExamAttempt
from extensions import db
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def admin_panel():
    total_users = User.query.count()
    total_exams = ExamAttempt.query.filter_by(completed=True).count()
    total_questions = Question.query.count()
    
    recent_exams = ExamAttempt.query.filter_by(completed=True).order_by(
        ExamAttempt.end_time.desc()
    ).limit(10).all()
    
    return render_template('admin/panel.html',
                         total_users=total_users,
                         total_exams=total_exams,
                         total_questions=total_questions,
                         recent_exams=recent_exams)

@admin_bp.route('/questions')
@login_required
@admin_required
def questions():
    all_questions = Question.query.all()
    return render_template('admin/questions.html', questions=all_questions)

@admin_bp.route('/add-question', methods=['POST'])
@login_required
@admin_required
def add_question():
    question_text = request.form.get('question_text')
    question_type = request.form.get('question_type')
    difficulty = request.form.get('difficulty')
    points = int(request.form.get('points', 10))
    
    question = Question(
        question_text=question_text,
        question_type=question_type,
        difficulty=difficulty,
        points=points
    )
    
    if question_type == 'multiple_choice':
        question.option_a = request.form.get('option_a')
        question.option_b = request.form.get('option_b')
        question.option_c = request.form.get('option_c')
        question.option_d = request.form.get('option_d')
        question.correct_answer = request.form.get('correct_answer')
    
    db.session.add(question)
    db.session.commit()
    
    flash('Soru başarıyla eklendi!', 'success')
    return redirect(url_for('admin.questions'))

@admin_bp.route('/generate-questions', methods=['POST'])
@login_required
@admin_required
def generate_questions():
    from utils.ai_generator import generate_questions_with_ai
    
    topic = request.form.get('topic', 'Python programlama')
    difficulty = request.form.get('difficulty', 'intermediate')
    count = int(request.form.get('count', 5))
    
    try:
        questions = generate_questions_with_ai(topic, difficulty, count)
        flash(f'{len(questions)} soru başarıyla oluşturuldu!', 'success')
    except Exception as e:
        flash(f'Soru oluşturulurken hata: {str(e)}', 'danger')
    
    return redirect(url_for('admin.questions'))

@admin_bp.route('/exam-results')
@login_required
@admin_required
def exam_results():
    # Get filter parameters
    level_filter = request.args.get('level', 'all')
    user_filter = request.args.get('user', '')
    
    # Base query
    query = ExamAttempt.query.filter_by(completed=True)
    
    # Apply filters
    if level_filter != 'all':
        query = query.filter_by(exam_level=level_filter)
    
    if user_filter:
        query = query.join(User).filter(User.username.contains(user_filter))
    
    # Get results ordered by date
    exam_attempts = query.order_by(ExamAttempt.end_time.desc()).all()
    
    # Calculate statistics
    stats = {
        'total': ExamAttempt.query.filter_by(completed=True).count(),
        'none': ExamAttempt.query.filter_by(completed=True, exam_level='none').count(),
        'beginner': ExamAttempt.query.filter_by(completed=True, exam_level='beginner').count(),
        'intermediate': ExamAttempt.query.filter_by(completed=True, exam_level='intermediate').count(),
        'advanced': ExamAttempt.query.filter_by(completed=True, exam_level='advanced').count(),
        'avg_score': db.session.query(db.func.avg(ExamAttempt.score)).filter_by(completed=True).scalar() or 0
    }
    
    return render_template('admin/exam_results.html',
                         exam_attempts=exam_attempts,
                         stats=stats,
                         level_filter=level_filter,
                         user_filter=user_filter)

@admin_bp.route('/exam-detail/<int:attempt_id>')
@login_required
@admin_required
def exam_detail(attempt_id):
    exam_attempt = ExamAttempt.query.get_or_404(attempt_id)
    return render_template('admin/exam_detail.html', exam_attempt=exam_attempt)
