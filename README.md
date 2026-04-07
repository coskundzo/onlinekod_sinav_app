# 🎓 onlinekod.com - Bursluluk Sınavı Platformu

Online bursluluk sınavı platformu ile öğrencilerin becerilerini test edin ve seviyelerini ölçün!

## ✨ Özellikler

- 👤 **Kullanıcı Kayıt ve Giriş Sistemi**
- 🔐 **Google OAuth ile Giriş** (Google ile Devam Et)
- 📱 **Telefon Numarası Kayıt** sistemi
- ⏱️ **25 Dakikalık Zamanlı Sınav**
- 📝 **Çoktan Seçmeli ve Kodlama Soruları**
- 🔀 **Rastgele Soru Seçimi** (20 soru, daha büyük soru bankasından)
- 🤖 **AI ile Otomatik Soru Üretimi** (OpenAI API)
- 💻 **Kod Editörü** ile programlama soruları
- 🔒 **Anti-Cheat Sistemi** (Sekme değişimi takibi)
- 📊 **Otomatik Değerlendirme**
- 🏆 **Liderlik Tablosu**
- 📜 **PDF Sertifika** oluşturma
- 🎨 **Seviye Sistemi** (Başlangıç 🟢 / Orta 🟡 / İleri 🔴)
- 👨‍💼 **Admin Paneli** soru yönetimi için

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- pip

### Adımlar

1. **Sanal ortam oluşturun:**
```bash
python -m venv venv
```

2. **Sanal ortamı aktif edin:**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Ortam değişkenlerini ayarlayın:**

`.env.example` dosyasını `.env` olarak kopyalayın:
```bash
copy .env.example .env
```

`.env` dosyasını düzenleyin:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///exams.db
OPENAI_API_KEY=your-openai-api-key-here-optional
FLASK_ENV=development
```

5. **Veritabanını oluşturun:**
```bash
python init_db.py
```

6. **Uygulamayı çalıştırın:**
```bash
python app.py
```

Uygulama `http://127.0.0.1:5000` adresinde çalışacaktır.

## 📖 Kullanım

### İlk Admin Kullanıcısı Oluşturma

1. Normal bir kullanıcı olarak kayıt olun
2. SQLite veritabanında (`exams.db`) bu kullanıcının `is_admin` değerini `1` yapın:

```sql
UPDATE user SET is_admin = 1 WHERE username = 'your_username';
```

Veya `init_db.py` scriptini kullanarak otomatik admin oluşturabilirsiniz.

### Sınav Akışı

1. Kullanıcı kayıt olur
2. "Sınava Başla" butonuna tıklar
3. 25 dakikalık timer başlar
4. Sorular sırayla gösterilir (çoktan seçmeli ve/veya kodlama)
5. "Sınavı Bitir" ile sınav tamamlanır
6. Sonuçlar ve seviye gösterilir
7. PDF sertifika indirilebilir

### Admin Paneli

Admin kullanıcılar:
- Soru ekleyebilir (manuel veya AI ile)
- Soru bankasını yönetebilir
- Kullanıcı istatistiklerini görüntüleyebilir
- Son sınavları takip edebilir

## 🤖 AI Soru Üretimi

OpenAI API kullanarak otomatik soru üretimi:

1. `.env` dosyasına OpenAI API anahtarınızı ekleyin
2. Admin panelinden "AI ile Soru Üret" seçeneğini kullanın
3. Konu, zorluk seviyesi ve soru sayısını belirtin

**Not:** API anahtarı yoksa, sistem otomatik olarak hazır sorular ekler.

## 📊 Seviye Sistemi

Puan aralıklarına göre seviye belirleme:

- 🟢 **Başlangıç**: 40% - 69%
- 🟡 **Orta**: 70% - 89%
- 🔴 **İleri**: 90% - 100%

## 🔒 Anti-Cheat Özellikleri

- Sekme değişimi takibi (max 3 uyarı)
- Sağ tık engelleme
- Kopyala/yapıştır kısıtlamaları (kod editörü hariç)
- Süre takibi

## 📁 Proje Yapısı

```
yeteneksinaviApp/
├── app.py                 # Ana uygulama
├── config.py              # Konfigürasyon
├── models.py              # Veritabanı modelleri
├── forms.py               # WTForms
├── requirements.txt       # Bağımlılıklar
├── init_db.py            # Veritabanı başlatma
├── routes/               # Route'lar (blueprints)
│   ├── auth.py           # Kimlik doğrulama
│   ├── main.py           # Ana sayfalar
│   ├── exam.py           # Sınav işlemleri
│   └── admin.py          # Admin paneli
├── templates/            # HTML şablonları
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── leaderboard.html
│   ├── auth/
│   ├── exam/
│   └── admin/
└── utils/                # Yardımcı fonksiyonlar
    ├── certificate.py    # PDF sertifika
    └── ai_generator.py   # AI soru üretimi
```

## 🛠️ Teknolojiler

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: Bootstrap 5, jQuery
- **Veritabanı**: SQLite (geliştirme), PostgreSQL önerilir (production)
- **PDF**: ReportLab
- **AI**: OpenAI GPT-3.5

## 🚀 Production Deployment

Production için öneriler:

1. PostgreSQL kullanın
2. Güvenli SECRET_KEY oluşturun
3. HTTPS kullanın
4. Gunicorn ile çalıştırın:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
5. Nginx reverse proxy kullanın

## 📝 Lisans

Bu proje eğitim amaçlıdır.

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing`)
5. Pull Request açın

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

---

Made with ❤️ using Flask
