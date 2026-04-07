import os
import openai
from models import Question
from extensions import db
from config import Config

def generate_questions_with_ai(topic="Python programlama", difficulty="intermediate", count=5):
    """
    Generate questions using OpenAI API.
    Falls back to predefined questions if API is not available.
    """
    
    api_key = Config.OPENAI_API_KEY
    
    if not api_key or api_key == 'your-openai-api-key-here-optional':
        # Fallback to predefined questions
        return generate_predefined_questions(topic, difficulty, count)
    
    try:
        openai.api_key = api_key
        
        prompt = f"""
        {count} adet {difficulty} seviyesinde {topic} konusunda çoktan seçmeli soru oluştur.
        Her soru için 4 seçenek (A, B, C, D) ve doğru cevabı da belirt.
        
        Format:
        SORU: [soru metni]
        A) [seçenek]
        B) [seçenek]
        C) [seçenek]
        D) [seçenek]
        CEVAP: [A/B/C/D]
        ---
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen bir eğitim uzmanısın ve kaliteli sınav soruları hazırlıyorsun."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        questions = parse_ai_questions(content, difficulty)
        
        # Save to database
        for q_data in questions:
            question = Question(
                question_text=q_data['question'],
                question_type='multiple_choice',
                difficulty=difficulty,
                option_a=q_data['options']['a'],
                option_b=q_data['options']['b'],
                option_c=q_data['options']['c'],
                option_d=q_data['options']['d'],
                correct_answer=q_data['correct'],
                points=10,
                is_ai_generated=True
            )
            db.session.add(question)
        
        db.session.commit()
        return questions
        
    except Exception as e:
        print(f"AI generation failed: {e}")
        return generate_predefined_questions(topic, difficulty, count)

def parse_ai_questions(content, difficulty):
    """Parse AI-generated questions"""
    questions = []
    blocks = content.split('---')
    
    for block in blocks:
        if 'SORU:' not in block:
            continue
            
        try:
            lines = block.strip().split('\n')
            question_text = ""
            options = {}
            correct = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith('SORU:'):
                    question_text = line.replace('SORU:', '').strip()
                elif line.startswith('A)'):
                    options['a'] = line[2:].strip()
                elif line.startswith('B)'):
                    options['b'] = line[2:].strip()
                elif line.startswith('C)'):
                    options['c'] = line[2:].strip()
                elif line.startswith('D)'):
                    options['d'] = line[2:].strip()
                elif line.startswith('CEVAP:'):
                    correct = line.replace('CEVAP:', '').strip().lower()
            
            if question_text and len(options) == 4 and correct:
                questions.append({
                    'question': question_text,
                    'options': options,
                    'correct': correct
                })
        except:
            continue
    
    return questions

def generate_predefined_questions(topic, difficulty, count):
    """Generate predefined questions when AI is not available"""
    
    predefined = [
        {
            'question': 'Python\'da liste oluşturmak için hangi parantez kullanılır?',
            'options': {
                'a': '{ }',
                'b': '[ ]',
                'c': '( )',
                'd': '< >'
            },
            'correct': 'b',
            'difficulty': 'beginner'
        },
        {
            'question': 'Aşağıdakilerden hangisi Python\'da değişken tanımlamak için geçerli bir addır?',
            'options': {
                'a': '123variable',
                'b': 'my-variable',
                'c': 'my_variable',
                'd': 'my variable'
            },
            'correct': 'c',
            'difficulty': 'beginner'
        },
        {
            'question': 'Python\'da "==" operatörü ne işe yarar?',
            'options': {
                'a': 'Değer ataması yapar',
                'b': 'Değerleri karşılaştırır',
                'c': 'Değerleri toplar',
                'd': 'Değişken tanımlar'
            },
            'correct': 'b',
            'difficulty': 'beginner'
        },
        {
            'question': 'Hangi fonksiyon bir listenin uzunluğunu döndürür?',
            'options': {
                'a': 'size()',
                'b': 'count()',
                'c': 'length()',
                'd': 'len()'
            },
            'correct': 'd',
            'difficulty': 'intermediate'
        },
        {
            'question': 'Python\'da dictionary tanımlamak için hangi karakterler kullanılır?',
            'options': {
                'a': '[ ]',
                'b': '( )',
                'c': '{ }',
                'd': '< >'
            },
            'correct': 'c',
            'difficulty': 'intermediate'
        },
        {
            'question': 'lambda fonksiyonu ne işe yarar?',
            'options': {
                'a': 'Döngü oluşturur',
                'b': 'Anonim fonksiyon tanımlar',
                'c': 'Değişken oluşturur',
                'd': 'Sınıf tanımlar'
            },
            'correct': 'b',
            'difficulty': 'advanced'
        },
    ]
    
    # Filter by difficulty and limit
    filtered = [q for q in predefined if q['difficulty'] == difficulty]
    if not filtered:
        filtered = predefined
    
    selected = filtered[:min(count, len(filtered))]
    
    # Save to database
    for q_data in selected:
        # Check if already exists
        existing = Question.query.filter_by(question_text=q_data['question']).first()
        if not existing:
            question = Question(
                question_text=q_data['question'],
                question_type='multiple_choice',
                difficulty=q_data['difficulty'],
                option_a=q_data['options']['a'],
                option_b=q_data['options']['b'],
                option_c=q_data['options']['c'],
                option_d=q_data['options']['d'],
                correct_answer=q_data['correct'],
                points=10,
                is_ai_generated=False
            )
            db.session.add(question)
    
    db.session.commit()
    return selected
