# PostgreSQL Kurulum Rehberi

## Windows için PostgreSQL Kurulumu

### 1. PostgreSQL İndir ve Kur

1. https://www.postgresql.org/download/windows/ adresine gidin
2. "Download the installer" linkine tıklayın
3. En son PostgreSQL versiyonunu indirin (örn: PostgreSQL 15 veya 16)
4. İndirdiğiniz installer'ı çalıştırın
5. Kurulum sırasında:
   - **Port**: 5432 (varsayılan)
   - **Password**: Unutmayacağınız bir şifre belirleyin (örn: `postgres123`)
   - **Locale**: Turkish, Turkey
   - pgAdmin 4'ü de kurmayı seçin (database yönetimi için)

### 2. PostgreSQL Servisini Başlatın

PostgreSQL kurulumdan sonra otomatik başlar. Kontrol için:

```powershell
# Servisi kontrol et
Get-Service -Name postgresql*

# Servis durumunu görmek için
sc query postgresql-x64-15  # veya kurduğunuz version
```

### 3. Database Oluşturun

#### Yöntem A: pgAdmin ile (Kolay)

1. pgAdmin 4'ü açın
2. Sol panelde "Servers" > "PostgreSQL" > sağ tık > "Create" > "Database"
3. Database adı: `online_sinav_db`
4. Owner: postgres
5. "Save" butonuna tıklayın

#### Yöntem B: Komut satırı ile

```powershell
# psql'e giriş yapın
psql -U postgres

# Database oluşturun
CREATE DATABASE online_sinav_db;

# Çıkış
\q
```

### 4. Environment Variables Ayarlayın

`.env` dosyası oluşturun (`.env.example` dosyasını kopyalayın):

```powershell
Copy-Item .env.example .env
```

`.env` dosyasını düzenleyin:

```env
SECRET_KEY=your-secret-key-change-this
DATABASE_URL=postgresql://postgres:SIFRENIZ@localhost:5432/online_sinav_db
OPENAI_API_KEY=your-openai-api-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

**Önemli**: `SIFRENIZ` kısmını PostgreSQL kurulumu sırasında belirlediğiniz şifre ile değiştirin!

### 5. Python Packages Güncelleyin

```powershell
# Virtual environment'ı aktif edin
.\venv\Scripts\Activate.ps1

# psycopg2-binary yükleyin (PostgreSQL driver)
pip install psycopg2-binary

# veya tüm requirements'ları güncelleyin
pip install -r requirements.txt
```

### 6. Database Tablolarını Oluşturun

```powershell
# Flask shell ile
python
```

Python shell'de:
```python
from app import create_app
from extensions import db

app = create_app()
with app.app_context():
    db.create_all()
    print("Database tabloları oluşturuldu!")
```

veya

```powershell
# Alternatif: init_db.py kullanın
python init_db.py
```

### 7. Uygulamayı Çalıştırın

```powershell
python app.py
```

Tarayıcıda http://localhost:5000 adresini açın.

## Sorun Giderme

### Problem 1: "psycopg2" bulunamadı
**Çözüm:**
```powershell
pip install psycopg2-binary
```

### Problem 2: PostgreSQL'e bağlanamıyor
**Çözüm:**
1. PostgreSQL servisinin çalıştığını kontrol edin:
   ```powershell
   Get-Service -Name postgresql*
   ```
2. Eğer çalışmıyorsa başlatın:
   ```powershell
   Start-Service postgresql-x64-15  # veya sizin version
   ```

### Problem 3: "password authentication failed"
**Çözüm:**
- `.env` dosyasındaki şifrenizi kontrol edin
- PostgreSQL kurulumu sırasında belirlediğiniz şifreyi kullandığınızdan emin olun

### Problem 4: Port 5432 kullanımda
**Çözüm:**
```powershell
# 5432 portunu kullanan uygulamayı bulun
netstat -ano | findstr :5432

# Veya farklı bir port kullanın
DATABASE_URL=postgresql://postgres:password@localhost:5433/online_sinav_db
```

### Problem 5: "database does not exist"
**Çözüm:**
```powershell
# psql ile database oluşturun
psql -U postgres
CREATE DATABASE online_sinav_db;
\q
```

## PostgreSQL Komutları

### psql Komutları

```powershell
# PostgreSQL shell'e giriş
psql -U postgres -d online_sinav_db

# Database'leri listele
\l

# Tabloları listele
\dt

# Tablo detaylarını göster
\d table_name

# Kullanıcıları listele
\du

# Çıkış
\q
```

### SQL Komutları

```sql
-- Tüm tabloları göster
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Kullanıcıları göster
SELECT * FROM "user";

-- Soruları göster
SELECT * FROM question LIMIT 10;

-- Database boyutu
SELECT pg_size_pretty(pg_database_size('online_sinav_db'));

-- Tablo boyutları
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Backup ve Restore

### Backup Alma

```powershell
# Tüm database
pg_dump -U postgres -d online_sinav_db -f backup.sql

# Sadece data (şema olmadan)
pg_dump -U postgres -d online_sinav_db --data-only -f data_backup.sql

# Compressed backup
pg_dump -U postgres -d online_sinav_db -F c -f backup.dump
```

### Restore Etme

```powershell
# SQL dosyasından
psql -U postgres -d online_sinav_db -f backup.sql

# Compressed backup'tan
pg_restore -U postgres -d online_sinav_db backup.dump
```

## Migration (Flask-Migrate)

Eğer database şemanızı değiştiriyorsanız:

```powershell
# İlk migration (tek sefer)
flask db init

# Migration oluştur
flask db migrate -m "Açıklama"

# Migration'ı uygula
flask db upgrade

# Geri al
flask db downgrade
```

## Performans İpuçları

1. **Index'ler**: Sık sorgulanan kolonlara index ekleyin
2. **Connection Pooling**: SQLAlchemy varsayılan olarak pool kullanır
3. **Query Optimization**: N+1 probleminden kaçının (joinedload kullanın)

## Yararlı Linkler

- PostgreSQL Documentation: https://www.postgresql.org/docs/
- pgAdmin Documentation: https://www.pgadmin.org/docs/
- SQLAlchemy PostgreSQL: https://docs.sqlalchemy.org/en/20/dialects/postgresql.html
