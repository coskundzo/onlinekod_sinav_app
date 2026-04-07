# Yetenek Sınav Platformu - Hızlı Başlangıç

## 🚀 Hızlı Kurulum (5 Dakika)

### 1. Sanal Ortam Oluştur ve Aktif Et

```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Bağımlılıkları Yükle

```powershell
pip install -r requirements.txt
```

### 3. .env Dosyası Oluştur

```powershell
copy .env.example .env
```

.env dosyasını aç ve gerekirse düzenle (varsayılan ayarlar yeterli):
```
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///exams.db
OPENAI_API_KEY=your-openai-api-key-here-optional
FLASK_ENV=development
```

### 4. Veritabanını Başlat

```powershell
python init_db.py
```

Bu komut:
- Veritabanı tablolarını oluşturur
- Admin kullanıcısı oluşturur (username: admin, password: admin123)
- 6 örnek soru ekler

### 5. Uygulamayı Çalıştır

```powershell
python app.py
```

### 6. Tarayıcıda Aç

http://127.0.0.1:5000

## 🎯 İlk Adımlar

1. **Admin olarak giriş yap:**
   - Kullanıcı adı: `admin`
   - Şifre: `admin123`

2. **Admin paneline git:**
   - Menüden "Admin" → "AI ile Soru Üret" veya "Manuel Soru Ekle"

3. **Normal kullanıcı oluştur:**
   - "Çıkış Yap" → "Kayıt Ol"
   - Yeni kullanıcı ile giriş yap

4. **Sınava başla:**
   - Dashboard'dan "Sınava Başla" butonuna tıkla
   - 25 dakikalık süre içinde sorulan 20 soruyu cevapla
   - "Sınavı Bitir" ile sonuçları gör

## 📝 Özellikler

✅ Kullanıcı kayıt/giriş sistemi
✅ 25 dakikalık zamanlı sınav (20 soru)
✅ Çoktan seçmeli sorular
✅ Otomatik değerlendirme
✅ Seviye belirleme (Başlangıç/Orta/İleri)
✅ Liderlik tablosu
✅ PDF sertifika
✅ Anti-cheat sistemi
✅ Admin paneli
✅ AI soru üretimi (OpenAI API ile)

## 🔧 Sorun Giderme

### ModuleNotFoundError hatası:
```powershell
pip install -r requirements.txt
```

### Database hatası:
```powershell
del exams.db
python init_db.py
```

### Port zaten kullanımda:
app.py dosyasındaki son satırı değiştir:
```python
app.run(debug=True, port=5001)
```

## 📚 Daha Fazla Bilgi

Detaylı kullanım için `README.md` dosyasına bakın.

## 🆘 Yardım

Herhangi bir sorun yaşarsanız:
1. `requirements.txt` dosyasındaki tüm paketlerin yüklü olduğundan emin olun
2. Python 3.8 veya üzeri sürüm kullanın
3. Sanal ortamın aktif olduğundan emin olun

---

Keyifli testler! 🎓
