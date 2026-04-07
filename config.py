import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-this'
    
    # Fix for Render PostgreSQL (postgres:// -> postgresql://)
    database_url = os.environ.get('DATABASE_URL') or 'sqlite:///exams.db'
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Google OAuth Settings
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    # Exam settings
    EXAM_DURATION = 30  # minutes
    QUESTIONS_PER_EXAM = 10
    
    # Level thresholds (percentage)
    BEGINNER_THRESHOLD = 40
    INTERMEDIATE_THRESHOLD = 70
    ADVANCED_THRESHOLD = 90
    
    # Anti-cheat settings
    MAX_TAB_SWITCHES = 3
