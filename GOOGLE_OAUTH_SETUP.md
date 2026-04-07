# Google OAuth Kurulum Rehberi

Bu rehber, uygulamanıza "Google ile Devam Et" özelliğini eklemek için gerekli adımları açıklar.

## 📋 Ön Gereksinimler

1. Google hesabı
2. Google Cloud Console erişimi

---

## 🔧 Kurulum Adımları

### 1. Google Cloud Console'da Proje Oluşturma

1. [Google Cloud Console](https://console.cloud.google.com/) adresine gidin
2. Yeni bir proje oluşturun veya mevcut projeyi seçin
3. Sol menüden **APIs & Services** > **Credentials** seçeneğine gidin

### 2. OAuth 2.0 Client ID Oluşturma

1. **CREATE CREDENTIALS** butonuna tıklayın
2. **OAuth client ID** seçeneğini seçin
3. Application type olarak **Web application** seçin
4. İsim verin (örn: "Yetenek Sınavı App")

### 3. Authorized Redirect URIs Ekleme

Aşağıdaki URL'leri **Authorized redirect URIs** bölümüne ekleyin:

**Geliştirme (Development):**
```
http://localhost:5000/auth/google-callback
http://127.0.0.1:5000/auth/google-callback
```

**Production (Canlı Site):**
```
https://yourdomain.com/auth/google-callback
```

### 4. OAuth Consent Screen Yapılandırması

1. **OAuth consent screen** sekmesine gidin
2. **User Type**: External seçin
3. **App name**: Uygulamanızın adını girin
4. **User support email**: Destek e-postanızı girin
5. **Developer contact information**: İletişim e-postanızı girin
6. **Scopes** bölümünde şunları ekleyin:
   - `.../auth/userinfo.email`
   - `.../auth/userinfo.profile`
   - `openid`

### 5. Client ID ve Secret'ı Alma

1. Credentials sayfasında oluşturduğunuz OAuth 2.0 Client ID'ye tıklayın
2. **Client ID** ve **Client Secret** değerlerini kopyalayın

---

## 🔐 Uygulama Konfigürasyonu

### 1. .env Dosyası Oluşturma

Proje kök dizininde `.env` dosyası oluşturun veya düzenleyin:

```env
# Google OAuth Credentials
GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret_here

# Other config
SECRET_KEY=your-secret-key-here
```

⚠️ **ÖNEMLİ**: `.env` dosyasını asla git'e commit etmeyin!

### 2. .gitignore Kontrolü

`.gitignore` dosyanızda şunların olduğundan emin olun:

```
.env
*.db
__pycache__/
instance/
```

---

## 📦 Paket Kurulumu

Yeni bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

---

## 🗄️ Veritabanı Güncelleme

Google OAuth için gerekli kolonları ekleyin:

```bash
python add_google_column.py
```

---

## 🚀 Uygulamayı Başlatma

```bash
python app.py
```

Uygulama varsayılan olarak http://localhost:5000 adresinde çalışacaktır.

---

## ✅ Test Etme

1. http://localhost:5000/auth/login adresine gidin
2. **"Google ile Devam Et"** butonuna tıklayın
3. Google hesabınızı seçin
4. İzinleri onaylayın
5. Uygulamaya yönlendirilmelisiniz

---

## 🔒 Güvenlik Notları

1. **Client Secret'ı Gizli Tutun**: Asla kod deposuna eklemeyin
2. **HTTPS Kullanın**: Production'da mutlaka HTTPS kullanın
3. **Redirect URI'ları Sınırlayın**: Sadece güvendiğiniz domain'leri ekleyin
4. **Session Secret**: Güçlü bir SECRET_KEY kullanın

---

## 🐛 Sorun Giderme

### "redirect_uri_mismatch" Hatası

- Google Console'da tanımlı redirect URI ile uygulamadaki URI'ın tam olarak eşleştiğinden emin olun
- `http://` vs `https://` farkına dikkat edin
- URL sonundaki `/` karakterine dikkat edin

### "Invalid Client" Hatası

- Client ID ve Client Secret'ın doğru kopyalandığından emin olun
- `.env` dosyasının doğru konumda olduğunu kontrol edin

### Token Hatası

- OAuth Consent Screen'in yayınlandığından emin olun
- Scope'ların doğru eklendiğini kontrol edin

---

## 📱 Mobil ve Production Notları

**Production'a Alırken:**

1. Domain'inizi Google Console'da Authorized domains'e ekleyin
2. Production redirect URI'sini ekleyin
3. OAuth Consent Screen'i "Publishing status: In production" yapın
4. HTTPS kullandığınızdan emin olun

**Mobil App İçin:**

- Android: SHA-1 fingerprint ekleyin
- iOS: Bundle ID ekleyin

---

## 📚 Ek Kaynaklar

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Authlib Documentation](https://docs.authlib.org/)
- [Flask OAuth Tutorial](https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask)

---

## 💡 Özellikler

✅ Kullanıcılar Google hesabıyla hızlıca kayıt olabilir  
✅ Şifre hatırlama gereksiz  
✅ Güvenli ve modern authentication  
✅ Mevcut hesaplara Google bağlama desteği  

---

**Not**: Bu özellik ücretsiz Google Cloud kullanımı ile çalışır. Aylık kullanım limitleri için [Google Cloud Pricing](https://cloud.google.com/pricing) sayfasını inceleyin.
