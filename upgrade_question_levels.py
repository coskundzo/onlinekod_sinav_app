"""
Bazı soruları intermediate ve advanced olarak işaretle
"""
from app import create_app
from extensions import db
from models import Question

def upgrade_question_levels():
    app = create_app()
    
    with app.app_context():
        # Kodlama gerektiren soruları al
        coding_questions = Question.query.filter_by(requires_coding=True).all()
        
        print(f"📊 {len(coding_questions)} kodlama sorusu bulundu.\n")
        
        if len(coding_questions) > 0:
            # İlk 2 tanesi beginner kalsın
            # Sonraki 2 tanesi intermediate olsun
            # Son 2 tanesi advanced olsun
            
            for i, question in enumerate(coding_questions):
                if i < 2:
                    question.difficulty = 'beginner'
                    print(f"✓ Soru #{question.id} -> beginner")
                elif i < 4:
                    question.difficulty = 'intermediate'
                    print(f"✓ Soru #{question.id} -> intermediate")
                else:
                    question.difficulty = 'advanced'
                    print(f"✓ Soru #{question.id} -> advanced")
        
        db.session.commit()
        
        print(f"\n✅ Kodlama soruları seviyeye göre ayrıldı!")
        
        # İstatistik göster
        print("\n📈 Güncel Soru Dağılımı:")
        print(f"   🌱 Başlangıç (beginner): {Question.query.filter_by(difficulty='beginner').count()}")
        print(f"   🌳 Orta (intermediate): {Question.query.filter_by(difficulty='intermediate').count()}")
        print(f"   🏆 İleri (advanced): {Question.query.filter_by(difficulty='advanced').count()}")
        print(f"\n   Kodlama Soruları Dağılımı:")
        print(f"   🟢 Beginner: {Question.query.filter_by(requires_coding=True, difficulty='beginner').count()}")
        print(f"   🟡 Intermediate: {Question.query.filter_by(requires_coding=True, difficulty='intermediate').count()}")
        print(f"   🔴 Advanced: {Question.query.filter_by(requires_coding=True, difficulty='advanced').count()}")

if __name__ == '__main__':
    upgrade_question_levels()
