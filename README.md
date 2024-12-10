# Telegram'da sahte grup üyeleri oluşturma

Bu proje, Telegram gruplarında yöneticiler tarafından gönderilen mesajları takip ederek, bu mesajlara OpenAI GPT-4 kullanarak samimi, yazım hatalı ve doğal yorumlar ekleyen bir botu simüle eder. Yorumlar, belirli bir grup için JSON formatında döndürülür ve rastgele hesaplardan grup sohbetine gönderilir.

## Özellikler

- Telegram grup sohbetlerinde yöneticilerin gönderdiği mesajları takip eder.
- Yöneticilerin mesajlarına samimi, yazım hatalı yorumlar oluşturur.
- Yorumları OpenAI GPT-4 kullanarak üretir.
- Yorumlar rastgele hesaplardan gönderilir.
- Her yorum arasında rastgele gecikme ekler.
- Telegram API kullanarak birden fazla hesapla işlem yapar.

## Gereksinimler

Bu projeyi çalıştırabilmek için aşağıdaki kütüphanelerin yüklü olması gerekmektedir:

- **openai**: OpenAI GPT API'yi kullanmak için.
- **telethon**: Telegram botlarını ve kullanıcı hesaplarını yönetmek için.
- **asyncio**: Asenkron işlemleri yönetmek için.
- **re**: Metin düzenlemeleri yapmak için.
- **json**: JSON formatında veri işlemek için.

## Uyarı

Bu işlem hesaplarınızın kapanmasına sebep olabilir, önemli hesaplarınızı bu işlemler için kullanmayınız.

### Kütüphanelerin Kurulumu

Proje için gerekli Python kütüphanelerini yüklemek için aşağıdaki komutları kullanabilirsiniz:

```bash
pip install openai
pip install telethon
