"""
Add more logic and pattern questions for non-coders
"""
from app import create_app
from extensions import db
from models import Question

def add_logic_questions():
    app = create_app()
    
    with app.app_context():
        logic_questions = [
            {
                'question_text': '🔢 Sıradaki sayı nedir? 2, 4, 6, 8, ?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': '9',
                'option_b': '10',
                'option_c': '11',
                'option_d': '12',
                'correct_answer': 'b',
                'points': 10
            },
            {
                'question_text': '🧩 Hangi şekil farklı? ⭐⭐🔵⭐',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'Birinci yıldız',
                'option_b': 'İkinci yıldız',
                'option_c': 'Mavi daire',
                'option_d': 'Üçüncü yıldız',
                'correct_answer': 'c',
                'points': 10
            },
            {
                'question_text': '🎯 Mantık: Elma elmadır. Muz meyvedir. Elma da meyvedir. Bu mantık doğru mu?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'Evet, doğru',
                'option_b': 'Hayır, yanlış',
                'option_c': 'Bilmiyorum',
                'option_d': 'Bazen doğru',
                'correct_answer': 'a',
                'points': 10
            },
            {
                'question_text': '🔄 Bir işi 3 kez tekrarlamak istiyorsun. Hangi ifade bunu anlatır?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'Bir kez yap',
                'option_b': '3 kez tekrarla',
                'option_c': 'Hiç yapma',
                'option_d': 'Sürekli yap',
                'correct_answer': 'b',
                'points': 10
            },
            {
                'question_text': '🚦 Trafik ışığı: Yeşil ise geç, kırmızı ise dur. Sarı ise ne yapmalısın?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'Hızlan',
                'option_b': 'Yavaşla ve hazırlan',
                'option_c': 'Dur',
                'option_d': 'Geri git',
                'correct_answer': 'b',
                'points': 10
            },
            {
                'question_text': '🎲 Hangi sayı çift değildir? 2, 4, 7, 8',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': '2',
                'option_b': '4',
                'option_c': '7',
                'option_d': '8',
                'correct_answer': 'c',
                'points': 10
            },
            {
                'question_text': '🔍 Desen tanıma: ABC, DEF, GHI, ... Sıradaki nedir?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'JKL',
                'option_b': 'XYZ',
                'option_c': 'MNO',
                'option_d': 'PQR',
                'correct_answer': 'a',
                'points': 10
            },
            {
                'question_text': '📊 Sıralama: En küçükten en büyüğe hangi sıralama doğrudur? 5, 2, 8, 1',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': '5, 2, 8, 1',
                'option_b': '8, 5, 2, 1',
                'option_c': '1, 2, 5, 8',
                'option_d': '2, 1, 5, 8',
                'correct_answer': 'c',
                'points': 10
            },
            {
                'question_text': '🎨 Renk mantığı: Kırmızı + Mavi = ?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'Yeşil',
                'option_b': 'Mor',
                'option_c': 'Turuncu',
                'option_d': 'Sarı',
                'correct_answer': 'b',
                'points': 10
            },
            {
                'question_text': '🧮 Basit matematik: 10 elmam var, 3 tanesini yedim. Kaç elma kaldı?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': '3',
                'option_b': '10',
                'option_c': '7',
                'option_d': '13',
                'correct_answer': 'c',
                'points': 10
            },
            {
                'question_text': '⏰ Sıralı düşünme: Önce uyan, sonra giyin, sonra kahvaltı yap. Hangi sıra doğru?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'Kahvaltı → Uyan → Giyin',
                'option_b': 'Uyan → Giyin → Kahvaltı',
                'option_c': 'Giyin → Kahvaltı → Uyan',
                'option_d': 'Uyan → Kahvaltı → Giyin',
                'correct_answer': 'b',
                'points': 10
            },
            {
                'question_text': '🎯 Problem çözme: Kapı kilitli ve anahtar masada. Kapıyı açmak için ne yapmalısın?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'Kapıyı kır',
                'option_b': 'Anahtarı al ve kilidi aç',
                'option_c': 'Bekle',
                'option_d': 'Pencereden çık',
                'correct_answer': 'b',
                'points': 10
            },
            {
                'question_text': '🔢 Dört işlem: 5 + 3 × 2 = ?',
                'question_type': 'multiple_choice',
                'difficulty': 'intermediate',
                'requires_coding': False,
                'option_a': '16',
                'option_b': '11',
                'option_c': '13',
                'option_d': '10',
                'correct_answer': 'b',
                'points': 15
            },
            {
                'question_text': '🧠 Mantıksal düşünme: Tüm kediler hayvandır. Boncuk bir kedidir. Boncuk hayvan mıdır?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'Evet',
                'option_b': 'Hayır',
                'option_c': 'Belki',
                'option_d': 'Bilgi yok',
                'correct_answer': 'a',
                'points': 10
            },
            {
                'question_text': '📐 Geometri: Kaç kenarı var: Üçgen?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': '2',
                'option_b': '3',
                'option_c': '4',
                'option_d': '5',
                'correct_answer': 'b',
                'points': 10
            }
        ]
        
        added_count = 0
        for q_data in logic_questions:
            # Check if question already exists
            existing = Question.query.filter_by(question_text=q_data['question_text']).first()
            if not existing:
                question = Question(**q_data)
                db.session.add(question)
                added_count += 1
        
        db.session.commit()
        print(f"✓ {added_count} mantık ve desen sorusu eklendi")
        
        # Show stats
        total = Question.query.count()
        coding_required = Question.query.filter_by(requires_coding=True).count()
        non_coding = Question.query.filter_by(requires_coding=False).count()
        
        print(f"\n📊 Soru İstatistikleri:")
        print(f"   Toplam: {total}")
        print(f"   Kodlama gerektiren: {coding_required}")
        print(f"   Kodlama gerektirmeyen (mantık/görsel): {non_coding}")

if __name__ == '__main__':
    add_logic_questions()
