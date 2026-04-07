from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import ExamAttempt, Question, Answer
from extensions import db
from datetime import datetime, timedelta
import random
import json

exam_bp = Blueprint('exam', __name__)

@exam_bp.route('/pre-survey', methods=['GET', 'POST'])
@login_required
def pre_survey():
    """Survey before starting exam to determine user's coding knowledge"""
    if request.method == 'POST':
        coding_level = request.form.get('coding_level')
        current_user.coding_knowledge = coding_level
        db.session.commit()
        return redirect(url_for('exam.start_exam'))
    
    return render_template('exam/pre_survey.html')

@exam_bp.route('/start', methods=['POST', 'GET'])
@login_required
def start_exam():
    # Check if user needs to complete pre-survey
    if current_user.coding_knowledge == 'unknown':
        return redirect(url_for('exam.pre_survey'))
    
    # Check if user has an active exam
    active_exam = ExamAttempt.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).first()
    
    if active_exam:
        return redirect(url_for('exam.take_exam', attempt_id=active_exam.id))
    
    # Create new exam attempt
    exam_attempt = ExamAttempt(
        user_id=current_user.id,
        exam_level=current_user.coding_knowledge
    )
    db.session.add(exam_attempt)
    db.session.commit()
    
    # Select questions based on user's coding knowledge
    if current_user.coding_knowledge == 'none':
        # ONLY visual/logic/pattern questions for non-coders - NO CODING AT ALL
        questions = Question.query.filter_by(requires_coding=False).order_by(db.func.random()).limit(20).all()
        
        if not questions or len(questions) < 10:
            flash('Yeterli görsel/mantık sorusu bulunamadı. Lütfen admin ile iletişime geçin.', 'warning')
            return redirect(url_for('main.dashboard'))
            
    elif current_user.coding_knowledge == 'beginner':
        # 2 beginner coding + 18 visual/logic questions
        visual_questions = Question.query.filter_by(requires_coding=False).order_by(db.func.random()).limit(18).all()
        coding_questions = Question.query.filter_by(requires_coding=True, difficulty='beginner').order_by(db.func.random()).limit(2).all()
        questions = visual_questions + coding_questions
        
        # Fill to 20 if not enough
        if len(questions) < 20:
            filler = Question.query.filter_by(requires_coding=False).order_by(db.func.random()).limit(20 - len(questions)).all()
            questions.extend(filler)
        
        random.shuffle(questions)
        
    elif current_user.coding_knowledge == 'intermediate':
        # 2 beginner + 2 intermediate coding + 16 visual/logic
        visual_questions = Question.query.filter_by(requires_coding=False).order_by(db.func.random()).limit(16).all()
        beginner_coding = Question.query.filter_by(requires_coding=True, difficulty='beginner').order_by(db.func.random()).limit(2).all()
        intermediate_coding = Question.query.filter_by(requires_coding=True, difficulty='intermediate').order_by(db.func.random()).limit(2).all()
        questions = visual_questions + beginner_coding + intermediate_coding
        
        # Fill to 20 if not enough
        if len(questions) < 20:
            filler = Question.query.filter_by(requires_coding=False).order_by(db.func.random()).limit(20 - len(questions)).all()
            questions.extend(filler)
            
        random.shuffle(questions)
        
    else:  # advanced
        # All 6 coding questions (2 beginner + 2 intermediate + 2 advanced) + 14 visual/logic
        visual_questions = Question.query.filter_by(requires_coding=False).order_by(db.func.random()).limit(14).all()
        beginner_coding = Question.query.filter_by(requires_coding=True, difficulty='beginner').order_by(db.func.random()).limit(2).all()
        intermediate_coding = Question.query.filter_by(requires_coding=True, difficulty='intermediate').order_by(db.func.random()).limit(2).all()
        advanced_coding = Question.query.filter_by(requires_coding=True, difficulty='advanced').order_by(db.func.random()).limit(2).all()
        questions = visual_questions + beginner_coding + intermediate_coding + advanced_coding
        
        # Fill to 20 if not enough
        if len(questions) < 20:
            filler = Question.query.filter_by(requires_coding=False).order_by(db.func.random()).limit(20 - len(questions)).all()
            questions.extend(filler)
            
        random.shuffle(questions)
    
    if not questions:
        flash('Henüz soru bulunmuyor. Lütfen admin ile iletişime geçin.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Create answer placeholders
    for question in questions:
        answer = Answer(
            exam_attempt_id=exam_attempt.id,
            question_id=question.id
        )
        db.session.add(answer)
    
    db.session.commit()
    
    return redirect(url_for('exam.take_exam', attempt_id=exam_attempt.id))

@exam_bp.route('/take/<int:attempt_id>')
@login_required
def take_exam(attempt_id):
    exam_attempt = ExamAttempt.query.get_or_404(attempt_id)
    
    # Security check
    if exam_attempt.user_id != current_user.id:
        flash('Bu sınava erişim yetkiniz yok.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if exam_attempt.completed:
        return redirect(url_for('exam.results', attempt_id=attempt_id))
    
    # Check time limit
    elapsed_time = datetime.utcnow() - exam_attempt.start_time
    if elapsed_time > timedelta(minutes=25):
        return redirect(url_for('exam.submit', attempt_id=attempt_id))
    
    questions = []
    for answer in exam_attempt.answers:
        questions.append(answer.question.to_dict())
    
    return render_template('exam/take_exam.html', 
                         exam_attempt=exam_attempt,
                         questions=questions,
                         elapsed_seconds=int(elapsed_time.total_seconds()))

@exam_bp.route('/save-answer', methods=['POST'])
@login_required
def save_answer():
    data = request.json
    attempt_id = data.get('attempt_id')
    question_id = data.get('question_id')
    user_answer = data.get('answer')
    
    answer = Answer.query.filter_by(
        exam_attempt_id=attempt_id,
        question_id=question_id
    ).first()
    
    if answer and answer.exam_attempt.user_id == current_user.id:
        answer.user_answer = user_answer
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'success': False}), 400

@exam_bp.route('/report-tab-switch', methods=['POST'])
@login_required
def report_tab_switch():
    data = request.json
    attempt_id = data.get('attempt_id')
    
    exam_attempt = ExamAttempt.query.get(attempt_id)
    if exam_attempt and exam_attempt.user_id == current_user.id:
        exam_attempt.tab_switches += 1
        db.session.commit()
        
        if exam_attempt.tab_switches >= 3:
            return jsonify({'success': True, 'warning': 'excessive', 'message': 'Çok fazla sekme değiştirdiniz!'})
        
        return jsonify({'success': True, 'warning': 'normal'})
    
    return jsonify({'success': False}), 400

@exam_bp.route('/submit/<int:attempt_id>', methods=['POST', 'GET'])
@login_required
def submit(attempt_id):
    exam_attempt = ExamAttempt.query.get_or_404(attempt_id)
    
    if exam_attempt.user_id != current_user.id:
        flash('Bu sınava erişim yetkiniz yok.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if exam_attempt.completed:
        return redirect(url_for('exam.results', attempt_id=attempt_id))
    
    # Grade the exam
    for answer in exam_attempt.answers:
        if answer.question.question_type == 'multiple_choice':
            if answer.user_answer == answer.question.correct_answer:
                answer.is_correct = True
        # Coding questions would need code execution here
    
    exam_attempt.end_time = datetime.utcnow()
    exam_attempt.completed = True
    exam_attempt.calculate_score()
    
    db.session.commit()
    
    return redirect(url_for('exam.results', attempt_id=attempt_id))

@exam_bp.route('/results/<int:attempt_id>')
@login_required
def results(attempt_id):
    exam_attempt = ExamAttempt.query.get_or_404(attempt_id)
    
    if exam_attempt.user_id != current_user.id:
        flash('Bu sınava erişim yetkiniz yok.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if not exam_attempt.completed:
        flash('Sınav henüz tamamlanmadı.', 'warning')
        return redirect(url_for('exam.take_exam', attempt_id=attempt_id))
    
    return render_template('exam/results.html', exam_attempt=exam_attempt)

@exam_bp.route('/certificate/<int:attempt_id>')
@login_required
def certificate(attempt_id):
    from utils.certificate import generate_certificate
    
    exam_attempt = ExamAttempt.query.get_or_404(attempt_id)
    
    if exam_attempt.user_id != current_user.id:
        flash('Bu sınava erişim yetkiniz yok.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if not exam_attempt.completed:
        flash('Sınav henüz tamamlanmadı.', 'warning')
        return redirect(url_for('exam.take_exam', attempt_id=attempt_id))
    
    return generate_certificate(current_user, exam_attempt)
