"""
Add phone_number column to User table
"""
from app import create_app
from extensions import db
from sqlalchemy import text

def add_phone_column():
    app = create_app()
    
    with app.app_context():
        try:
            # Add phone_number column to user table
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE "user" ADD COLUMN phone_number VARCHAR(20)'))
                conn.commit()
            print("✓ phone_number sütunu başarıyla eklendi!")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("⚠️  phone_number sütunu zaten mevcut")
            else:
                print(f"❌ Hata: {e}")
                print("\nAlternatif: Veritabanını sıfırlamak için 'python init_db.py' komutunu çalıştırın")

if __name__ == '__main__':
    add_phone_column()
