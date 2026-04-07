from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)  # Nullable for OAuth users
    google_id = db.Column(db.String(255), unique=True, nullable=True)  # Google OAuth ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Coding knowledge level
    coding_knowledge = db.Column(db.String(20), default='unknown')  # 'none', 'beginner', 'intermediate', 'advanced', 'unknown'
    
    # Relationships
    exam_attempts = db.relationship('ExamAttempt', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_best_score(self):
        attempts = ExamAttempt.query.filter_by(user_id=self.id, completed=True).all()
        if not attempts:
            return 0
        return max(attempt.score for attempt in attempts)
    
    def get_level(self):
        best_score = self.get_best_score()
        if best_score >= 90:
            return 'advanced'
        elif best_score >= 70:
            return 'intermediate'
        elif best_score >= 40:
            return 'beginner'
        return 'none'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # 'multiple_choice', 'coding', 'visual', 'drag_drop', 'sequence'
    difficulty = db.Column(db.String(20), nullable=False)  # 'beginner', 'intermediate', 'advanced'
    requires_coding = db.Column(db.Boolean, default=True)  # Does this question require coding knowledge?
    
    # For multiple choice
    option_a = db.Column(db.Text)
    option_b = db.Column(db.Text)
    option_c = db.Column(db.Text)
    option_d = db.Column(db.Text)
    correct_answer = db.Column(db.String(1))  # 'a', 'b', 'c', 'd'
    
    # For coding questions
    test_cases = db.Column(db.Text)  # JSON string
    time_limit = db.Column(db.Integer, default=2)  # second
    
    # For visual/interactive questions
    visual_data = db.Column(db.Text)  # JSON string with visual elements, blocks, etc.
    correct_sequence = db.Column(db.Text)  # For sequence questions
    target_position = db.Column(db.Text)  # For drag-drop questionss
    memory_limit = db.Column(db.Integer, default=128)  # MB
    
    points = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_ai_generated = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        data = {
            'id': self.id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'difficulty': self.difficulty,
            'points': self.points
        }
        if self.question_type == 'multiple_choice':
            data['options'] = {
                'a': self.option_a,
                'b': self.option_b,
                'c': self.option_c,
                'd': self.option_d
            }
        return data

class ExamAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    score = db.Column(db.Float, default=0)
    max_score = db.Column(db.Float, default=100)
    completed = db.Column(db.Boolean, default=False)
    tab_switches = db.Column(db.Integer, default=0)
    exam_level = db.Column(db.String(20), default='unknown')  # none, beginner, intermediate, advanced
    
    # Relationships
    answers = db.relationship('Answer', backref='exam_attempt', lazy=True, cascade='all, delete-orphan')
    
    def calculate_score(self):
        total_points = 0
        earned_points = 0
        
        for answer in self.answers:
            total_points += answer.question.points
            if answer.is_correct:
                earned_points += answer.question.points
        
        if total_points > 0:
            self.score = (earned_points / total_points) * 100
            self.max_score = 100
        return self.score
    
    def get_level(self):
        if self.score >= 90:
            return 'advanced'
        elif self.score >= 70:
            return 'intermediate'
        elif self.score >= 40:
            return 'beginner'
        return 'none'
    
    def get_level_emoji(self):
        level = self.get_level()
        emojis = {
            'advanced': '🔴',
            'intermediate': '🟡',
            'beginner': '🟢',
            'none': '⚪'
        }
        return emojis.get(level, '⚪')

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_attempt_id = db.Column(db.Integer, db.ForeignKey('exam_attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_answer = db.Column(db.Text)
    is_correct = db.Column(db.Boolean, default=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    question = db.relationship('Question', backref='answers')
