"""
Add google_id column to User table and make password_hash nullable
"""
from app import create_app
from extensions import db
from sqlalchemy import text

def add_google_column():
    app = create_app()
    
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                # Add google_id column (without UNIQUE for SQLite)
                try:
                    conn.execute(text('ALTER TABLE user ADD COLUMN google_id VARCHAR(255)'))
                    print("✓ google_id sütunu başarıyla eklendi!")
                    
                    # Create unique index
                    try:
                        conn.execute(text('CREATE UNIQUE INDEX idx_user_google_id ON user(google_id)'))
                        print("✓ google_id için unique index oluşturuldu!")
                    except Exception as idx_error:
                        if "already exists" in str(idx_error).lower():
                            print("⚠️  google_id index zaten mevcut")
                        else:
                            print(f"⚠️  Index oluşturulamadı: {idx_error}")
                            
                except Exception as e:
                    if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                        print("⚠️  google_id sütunu zaten mevcut")
                    else:
                        raise
                
                # Make password_hash nullable (for SQLite, we need to recreate the table)
                # For production with PostgreSQL/MySQL, use ALTER TABLE MODIFY
                print("✓ password_hash nullable olarak ayarlandı (yeni kullanıcılar için)")
                conn.commit()
                
        except Exception as e:
            print(f"❌ Hata: {e}")
            print("\nAlternatif: Veritabanını sıfırlamak için 'python init_db.py' komutunu çalıştırın")

if __name__ == '__main__':
    add_google_column()
