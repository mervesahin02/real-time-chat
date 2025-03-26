# Triscord: Gerçek Zamanlı Sohbet Uygulaması

## Proje Genel Bakış

Triscord, PyQt5 grafik kullanıcı arayüzü ve PostgreSQL veri yönetimi ile oluşturulmuş zengin özelliklere sahip gerçek zamanlı bir sohbet uygulamasıdır. Uygulama güvenli kullanıcı kimlik doğrulama, özel mesajlaşma, emoji desteği ve sağlam dosya paylaşım yetenekleri sağlar.

## Özellikler

### Kullanıcı Yönetimi
- Güvenli kullanıcı kayıt ve giriş
- Gelişmiş güvenlik için parola karması
- Kullanıcı profili oluşturma ve yönetimi

### Mesajlaşma
- Gerçek zamanlı grup sohbeti
- Özel mesajlaşma
- Zaman damgalı mesaj günlüğü
- Emoji seçici

### Kullanıcı Deneyimi
- Dinamik çevrimiçi kullanıcı listesi
- Kullanıcı etkileşimleri için içerik menüsü
- Esnek UI tasarımı

### Veritabanı Entegrasyonu
- PostgreSQL veritabanı için:
  - Kullanıcı yönetimi
  - Mesaj geçmişi
  - Kullanıcı profilleri
  - Dosya paylaşım meta verileri

## Ön Gereksinimler

### Yazılım Gereksinimleri
- Python 3.8+
- PostgreSQL 12+
- Gerekli Python Kütüphaneleri:
  - PyQt5
  - psycopg2
  - socket
  - threading
  - uuid
  - hashlib

### Veritabanı Kurulumu
1. `triscord_db` adında bir PostgreSQL veritabanı oluşturun
2. PostgreSQL'in localhost:5432'de çalıştığından emin olun
3. Varsayılan kimlik bilgileri:
   - Kullanıcı Adı: postgres
   - Parola: HappyCat

## Kurulum

1. Depoyu klonlayın
```bash
git clone https://github.com/kullaniciadiniz/triscord.git
cd triscord
```

2. Bağımlılıkları yükleyin
```bash
pip install PyQt5 psycopg2 
```

3. Veritabanını Yapılandırın
- Gerekirse her sınıfın yapıcı metodunda bağlantı parametrelerini değiştirin
- PostgreSQL'in çalıştığından emin olun

## Uygulamayı Çalıştırma

```bash
python triscord.py
```

## Proje Yapısı

- `triscord.py`: Ana uygulama giriş noktası
- `server.py`: Gerçek zamanlı iletişim için soket sunucusu
- `user_manager.py`: Kullanıcı kimlik doğrulama ve kayıt
- `user_profiles.py`: Kullanıcı profili yönetimi
- `message_logger.py`: Mesaj geçmişi günlüğü
- `file_sharing.py`: Dosya yükleme ve meta veri izleme
- `styles.py`: UI stil yapılandırmaları

## Güvenlik Özellikleri

- SHA-256 ile parola karması
- Güvenli veritabanı bağlantı havuzu
- Benzersiz kullanıcı tanımlama
- Özel mesaj şifrelemesi

## Özelleştirme

- UI görünümünü değiştirmek için `styles.py`'yi düzenleyin
- İlgili sınıf yapıcılarında veritabanı bağlantı parametrelerini ayarlayın

## Planlanan İyileştirmeler

- Uçtan uca mesaj şifrelemesi
- Dosya transfer işlevselliği
- Gelişmiş kullanıcı profil özellikleri
- Gelişmiş hata işleme

## Katkıda Bulunma

1. Depoyu çatallayın
2. Özellik dalınızı oluşturun (`git checkout -b feature/MükemmelOzellik`)
3. Değişikliklerinizi kaydedin (`git commit -m 'MükemmelOzellik ekle'`)
4. Dala gönderin (`git push origin feature/MükemmelOzellik`)
5. Bir Çekme İsteği açın

## Lisans

MIT Lisansı altında dağıtılmaktadır. Daha fazla bilgi için `LICENSE`'a bakın.

## İletişim

Seyyide Merve Şahin - sydmervesihin@gmail.com

Proje Bağlantısı: [https://github.com/kullaniciadiniz/triscord](https://github.com/kullaniciadiniz/triscord)
