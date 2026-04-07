"""
Database initialization script
Creates tables and adds sample data including an admin user
"""

from app import create_app
from extensions import db
from models import User, Question
from utils.ai_generator import generate_predefined_questions

def init_database():
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creating admin user...")
            admin = User(
                username='admin',
                email='admin@example.com',
                phone_number='05001234567',
                is_admin=True
            )
            admin.set_password('admin123')  # Change this password!
            db.session.add(admin)
            db.session.commit()
            print(f"✓ Admin user created: username='admin', password='admin123'")
            print("⚠️  IMPORTANT: Change the admin password after first login!")
        else:
            print("Admin user already exists")
        
        # Check if questions exist
        question_count = Question.query.count()
        if question_count == 0:
            print("Adding sample questions...")
            try:
                # Add beginner questions
                generate_predefined_questions('Python', 'beginner', 3)
                # Add intermediate questions
                generate_predefined_questions('Python', 'intermediate', 2)
                # Add advanced questions
                generate_predefined_questions('Python', 'advanced', 1)
                print(f"✓ {Question.query.count()} sample questions added")
            except Exception as e:
                print(f"Error adding questions: {e}")
        else:
            print(f"Database already has {question_count} questions")
        
        print("\n" + "="*50)
        print("Database initialization complete!")
        print("="*50)
        print("\nYou can now run the application:")
        print("  python app.py")
        print("\nDefault admin credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\n⚠️  Remember to change the admin password!")
        print("="*50 + "\n")

if __name__ == '__main__':
    init_database()
