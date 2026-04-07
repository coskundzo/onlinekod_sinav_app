"""
Add visual/interactive questions for non-coders
"""
from app import create_app
from extensions import db
from models import Question

def add_visual_questions():
    app = create_app()
    
    with app.app_context():
        visual_questions = [
            {
                'question_text': '🧱 Blokları doğru sıraya yerleştir: Bir program yazmak için gerekli adımları sırala',
                'question_type': 'drag_drop',
                'difficulty': 'beginner',
                'requires_coding': False,
                'correct_answer': 'Başla,Değişken Oluştur,Döngü,Yazdır,Bitir',
                'points': 10
            },
            {
                'question_text': '🎯 Hedefe ulaş: Başlangıçtan hedefe giden yolu bul ve yıldızları topla',
                'question_type': 'visual',
                'difficulty': 'beginner',
                'requires_coding': False,
                'correct_answer': '0,4,5,9,13,14,15',
                'points': 15
            },
            {
                'question_text': '🧩 Doğru sırayı bul: Bir uygulamanın çalışma adımlarını sırala',
                'question_type': 'sequence',
                'difficulty': 'beginner',
                'requires_coding': False,
                'correct_answer': '0,1,2,3',
                'points': 10
            },
            {
                'question_text': 'Bir robotun hareket etmesi için hangi komutlar gerekir?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'İleri, Geri, Sağa Dön, Sola Dön',
                'option_b': 'Başla, Bitir',
                'option_c': 'Oku, Yaz',
                'option_d': 'Topla, Çıkar',
                'correct_answer': 'a',
                'points': 10
            },
            {
                'question_text': 'Bir döngü (loop) ne işe yarar?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'Bir işlemi sadece bir kez yapar',
                'option_b': 'Bir işlemi tekrar tekrar yapar',
                'option_c': 'Programı durdurur',
                'option_d': 'Ekrana yazı yazar',
                'correct_answer': 'b',
                'points': 10
            },
            {
                'question_text': 'Bir karakterin ekranda hareket etmesi için ne yapmalıyız?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'Karakterin konumunu değiştirmeliyiz',
                'option_b': 'Karakteri silmeliyiz',
                'option_c': 'Ekranı kapatmalıyız',
                'option_d': 'Hiçbir şey yapmamalıyız',
                'correct_answer': 'a',
                'points': 10
            },
            {
                'question_text': 'Aşağıdaki görsellerden hangisi değişken (variable) kavramını temsil eder?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': '📦 Bir kutu (içinde değer saklayan)',
                'option_b': '🔄 Bir ok (yön gösteren)',
                'option_c': '🎯 Bir hedef',
                'option_d': '⏹️ Bir dur işareti',
                'correct_answer': 'a',
                'points': 10
            },
            {
                'question_text': 'Bir oyunda "eğer puan 100\'den büyükse kazandın" mantığı hangi yapıya örnektir?',
                'question_type': 'multiple_choice',
                'difficulty': 'intermediate',
                'requires_coding': False,
                'option_a': 'Döngü (Loop)',
                'option_b': 'Koşul (If-Else)',
                'option_c': 'Değişken (Variable)',
                'option_d': 'Fonksiyon (Function)',
                'correct_answer': 'b',
                'points': 15
            },
            {
                'question_text': '🎮 Bir oyunda karakterin zıplaması için hangi olayı dinlemeliyiz?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'Fare tıklaması veya tuş basımı',
                'option_b': 'Ekran kapanması',
                'option_c': 'Ses çalması',
                'option_d': 'Renk değişimi',
                'correct_answer': 'a',
                'points': 10
            },
            {
                'question_text': 'Aşağıdaki işlemlerden hangisi algoritmaya en iyi örnektir?',
                'question_type': 'multiple_choice',
                'difficulty': 'beginner',
                'requires_coding': False,
                'option_a': 'Rastgele sayılar seçmek',
                'option_b': 'Adım adım tarif takip ederek yemek yapmak',
                'option_c': 'Hiçbir plan olmadan ilerlemek',
                'option_d': 'Sadece sonuca bakmak',
                'correct_answer': 'b',
                'points': 10
            }
        ]
        
        added_count = 0
        for q_data in visual_questions:
            # Check if question already exists
            existing = Question.query.filter_by(question_text=q_data['question_text']).first()
            if not existing:
                question = Question(**q_data)
                db.session.add(question)
                added_count += 1
        
        db.session.commit()
        print(f"✓ {added_count} görsel/interaktif soru eklendi")
        print(f"Toplam soru sayısı: {Question.query.count()}")

if __name__ == '__main__':
    add_visual_questions()
