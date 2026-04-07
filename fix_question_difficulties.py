"""
Mevcut sorulara difficulty (zorluk seviyesi) ekle/düzelt
"""
from app import create_app
from extensions import db
from models import Question

def fix_question_difficulties():
    app = create_app()
    
    with app.app_context():
        # Tüm soruları al
        questions = Question.query.all()
        
        print(f"📊 Toplam {len(questions)} soru bulundu.\n")
        
        updated_count = 0
        
        for question in questions:
            # Eğer difficulty yoksa veya yanlışsa düzelt
            if not question.difficulty or question.difficulty not in ['beginner', 'intermediate', 'advanced']:
                # Görsel/mantık soruları genelde başlangıç seviyesi
                if not question.requires_coding:
                    question.difficulty = 'beginner'
                    print(f"✓ Soru #{question.id} (Görsel/Mantık) -> beginner")
                    updated_count += 1
                # Kodlama soruları için varsayılan orta seviye
                else:
                    question.difficulty = 'intermediate'
                    print(f"✓ Soru #{question.id} (Kodlama) -> intermediate")
                    updated_count += 1
        
        db.session.commit()
        
        print(f"\n✅ {updated_count} soru güncellendi!")
        
        # İstatistik göster
        print("\n📈 Soru Dağılımı:")
        print(f"   🌱 Başlangıç (beginner): {Question.query.filter_by(difficulty='beginner').count()}")
        print(f"   🌳 Orta (intermediate): {Question.query.filter_by(difficulty='intermediate').count()}")
        print(f"   🏆 İleri (advanced): {Question.query.filter_by(difficulty='advanced').count()}")
        print(f"\n   📝 Kodlama Gerektiren: {Question.query.filter_by(requires_coding=True).count()}")
        print(f"   🧩 Mantık/Görsel: {Question.query.filter_by(requires_coding=False).count()}")

if __name__ == '__main__':
    fix_question_difficulties()
