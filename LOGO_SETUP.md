# 📸 Logo Kurulumu - onlinekod.com

## Sertifikaya Logo Ekleme

Sertifikalarda onlinekod.com logosunu göstermek için aşağıdaki adımları izleyin:

### 1. Logo Dosyasını Hazırlama

Logo dosyanızı **PNG formatında** hazırlayın:
- **Önerilen boyut**: 400x120 piksel (veya 10:3 oranı)
- **Arka plan**: Şeffaf (transparent) tercih edilir
- **Format**: PNG (yüksek kalite)

### 2. Logo Dosyasını Projeye Ekleme

Logo dosyasını şu konuma kaydedin:
```
yeteneksinaviApp/
  static/
    images/
      onlinekod_logo.png    ← Logoyu buraya kaydedin
```

### 3. Logo Adlandırma

Logo dosyasının adı **tam olarak** şu şekilde olmalıdır:
```
onlinekod_logo.png
```

### 4. Alternatif Logo Formatları

Eğer farklı bir format kullanmak isterseniz, `utils/certificate.py` dosyasını düzenleyebilirsiniz:

```python
# 89. satır civarında:
logo_path = os.path.join('static', 'images', 'onlinekod_logo.png')
```

Bu satırı değiştirerek `.jpg`, `.jpeg` veya başka formatlar kullanabilirsiniz.

### 5. Test Etme

Logo ekledikten sonra:
1. Bir sınav tamamlayın
2. Sertifika indirin
3. PDF'i açın ve logo görünüyor mu kontrol edin

### 6. Logo Yoksa Ne Olur?

Logo dosyası yoksa veya yüklenemezse, sistem otomatik olarak **text-based header** gösterir:
```
ONLINEKOD.COM
Bursluluk Sınavı
```

---

## 🎨 Mevcut Logo

Eklediğiniz logo görselini kullanarak:
1. Görseli **onlinekod_logo.png** olarak kaydedin
2. **static/images/** klasörüne taşıyın
3. Uygulamayı yeniden başlatın (gerekirse)

## 📝 Not

- Logo boyutu sertifikada otomatik olarak **2 inch genişlik** olacak şekilde ayarlanır
- Yükseklik orantılı olarak korunur (aspect ratio preserved)
- Logo kalitesi için yüksek çözünürlüklü PNG kullanın

## ✅ Tamamlandı

Logo başarıyla eklendiğinde, tüm yeni sertifikalarda otomatik olarak görünecektir!
