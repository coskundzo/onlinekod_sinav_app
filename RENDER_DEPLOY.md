# Render'da Deployment Rehberi

## Gerekli Dosyalar ✅

Aşağıdaki dosyalar projenize eklendi:
- ✅ `render.yaml` - Render otomatik yapılandırma dosyası
- ✅ `build.sh` - Build script
- ✅ `runtime.txt` - Python versiyonu
- ✅ `.gitignore` - Git ignore kuralları
- ✅ `requirements.txt` - psycopg2-binary eklendi
- ✅ `config.py` - PostgreSQL URL düzeltmesi eklendi
- ✅ `app.py` - Gunicorn için app instance eklendi

## Deployment Adımları

### 1. Git Repository'i Hazırlayın

```bash
# Eğer henüz git init yapmadıysanız:
git init

# Değişiklikleri commit edin:
git add .
git commit -m "Render deployment için yapılandırma eklendi"

# GitHub'a push edin:
git remote add origin https://github.com/KULLANICI_ADI/REPO_ADI.git
git branch -M main
git push -u origin main
```

### 2. Render Hesabı Oluşturun

1. https://render.com adresine gidin
2. GitHub hesabınızla giriş yapın
3. Render'a GitHub repository'lerinize erişim izni verin

### 3. Yeni Web Service Oluşturun

#### Seçenek A: Otomatik (render.yaml ile - ÖNERİLEN)

1. Render Dashboard'da "New +" butonuna tıklayın
2. "Blueprint" seçeneğini seçin
3. GitHub repository'nizi seçin
4. `render.yaml` dosyası otomatik olarak tespit edilecektir
5. "Apply" butonuna tıklayın

#### Seçenek B: Manuel

1. Render Dashboard'da "New +" butonuna tıklayın
2. "Web Service" seçeneğini seçin
3. GitHub repository'nizi seçin
4. Aşağıdaki ayarları yapın:
   - **Name**: online-sinav-app (veya istediğiniz isim)
   - **Runtime**: Python
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free (başlangıç için)

### 4. PostgreSQL Database Oluşturun

1. Render Dashboard'da "New +" butonuna tıklayın
2. "PostgreSQL" seçeneğini seçin
3. Aşağıdaki bilgileri girin:
   - **Name**: online-sinav-db
   - **Database**: online_sinav
   - **User**: online_sinav_user
   - **Region**: En yakın bölgeyi seçin
   - **Instance Type**: Free
4. "Create Database" butonuna tıklayın
5. Database oluşturulduktan sonra "Internal Database URL" kopyalayın

### 5. Environment Variables Ayarlayın

Web Service'inizin ayarlarına gidip "Environment" sekmesinde aşağıdaki değişkenleri ekleyin:

```
DATABASE_URL = [PostgreSQL Internal Database URL'inizi buraya yapıştırın]
SECRET_KEY = [Güçlü bir rastgele anahtar - Render otomatik oluşturabilir]
OPENAI_API_KEY = [OpenAI API anahtarınız]
GOOGLE_CLIENT_ID = [Google OAuth Client ID]
GOOGLE_CLIENT_SECRET = [Google OAuth Client Secret]
```

**Önemli Notlar:**
- `DATABASE_URL`: PostgreSQL database'inizden alın (Internal Database URL)
- `SECRET_KEY`: Güvenli bir rastgele string kullanın. Python ile oluşturabilirsiniz:
  ```python
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- Google OAuth için `GOOGLE_CLIENT_ID` ve `GOOGLE_CLIENT_SECRET` gereklidir

### 6. Google OAuth Redirect URI Güncellemesi

Google Cloud Console'da OAuth 2.0 ayarlarınıza gidin ve **Authorized redirect URIs** kısmına Render URL'inizi ekleyin:

```
https://UYGULAMA_ADINIZ.onrender.com/auth/google/callback
```

### 7. Deploy Edin

- Manuel deploy için: "Manual Deploy" > "Deploy latest commit"
- Otomatik deploy: Her git push'ta otomatik deploy olacaktır

### 8. İlk Deployment Süresi

⏱️ İlk deployment 5-10 dakika sürebilir. Render:
1. Dependencies yükleyecek (requirements.txt)
2. Database tablolarını oluşturacak
3. Uygulamayı başlatacak

### 9. Logs Kontrol Edin

Deployment sırasında veya sonrasında hata varsa:
- Render Dashboard > Your Service > "Logs" sekmesine bakın
- Hataları burada görebilirsiniz

## Sık Karşılaşılan Sorunlar

### Problem: "postgres://" URL hatası
**Çözüm**: `config.py` dosyası otomatik olarak düzeltildi. postgres:// -> postgresql:// çevirimi yapılıyor.

### Problem: psycopg2 import hatası
**Çözüm**: `requirements.txt`'e `psycopg2-binary` eklendi.

### Problem: Database tablolarıoluşturulmadı
**Çözüm**: `build.sh` scripti otomatik olarak `db.create_all()` çalıştırıyor.

### Problem: Uygulama çalışmıyor
**Çözüm**: Logs kontrol edin ve environment variables'ların doğru ayarlandığından emin olun.

## Test Etme

Deploy başarılı olduktan sonra:
1. Render'ın verdiği URL'i açın (örn: https://online-sinav-app.onrender.com)
2. Kayıt olup giriş yapmayı deneyin
3. Sınav oluşturmayı test edin

## Önemli Notlar

- ⚠️ **Free tier**: İlk istek 30-60 saniye sürebilir (cold start)
- 💾 **Database**: Free PostgreSQL 1GB limit var
- 🔒 **HTTPS**: Render otomatik olarak SSL sertifikası sağlar
- 🔄 **Auto-deploy**: main branch'e her push otomatik deploy tetikler

## Destek

Sorun yaşarsanız:
- Render Docs: https://render.com/docs
- Render Community: https://community.render.com/

## Güncelleme

Kod değişikliklerini deploy etmek için:

```bash
git add .
git commit -m "Değişiklik açıklaması"
git push origin main
```

Render otomatik olarak yeni version'ı deploy edecektir.
