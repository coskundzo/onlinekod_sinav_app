"""
Add exam_level column to ExamAttempt table
"""
from app import create_app
from extensions import db
from sqlalchemy import text

def add_exam_level_column():
    app = create_app()
    
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                # Add exam_level column
                try:
                    conn.execute(text("ALTER TABLE exam_attempt ADD COLUMN exam_level VARCHAR(20) DEFAULT 'unknown'"))
                    print("✓ exam_level sütunu başarıyla eklendi!")
                except Exception as e:
                    if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                        print("⚠️  exam_level sütunu zaten mevcut")
                    else:
                        raise
                
                conn.commit()
                print("✓ Veritabanı migration tamamlandı!")
                
        except Exception as e:
            print(f"❌ Hata: {e}")
            print("\nAlternatif: Veritabanını sıfırlamak için 'python init_db.py' komutunu çalıştırın")

if __name__ == '__main__':
    add_exam_level_column()
