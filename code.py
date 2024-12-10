import openai
import random
import re
import time
import json
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio
import json
#--------------------------------------- AYARLAR ---------------------------------------------
'''
https://my.telegram.org # api_id ve api_hash bilgilerini buradan uygulama oluşturarak alabilirsiniz
'''

# OpenAI API anahtarınızı buraya ekleyin
openai.api_key = ' buraya '

# Hesap bilgileri
accounts = [
    {"api_id": "", "api_hash": "", "phone": "+"},
    {"api_id": "", "api_hash": "", "phone": "+"},
    # Diğer hesap bilgilerini buraya ekleyin...
]


group_link = 'cloudguys0' # Grubun kullanıcı adı veya davet linki
category = 'borsa' # Grubun kategorisi
description = 'grup açıklaması'# Grubun açıklaması
admin_icon = '💎' # Hesaplar admin bu icon'u mesaja eklediğinde cevap verirler

#--------------------------------------- AYARLAR SONU ---------------------------------------

def generate_messages_json(count):
    messages = {f"message{i}": f"Mesaj {i}" for i in range(1, count + 1)}
    return json.dumps(messages, separators=(",", ":"), ensure_ascii=False)

# Text analizi için OpenAI API fonksiyonu
def analyze_text(group_title,admin_message,message_count):
    json_text = generate_messages_json(message_count)
    system_message = (
        f'Adı: {group_title}, Kategorisi: {category}, Açıklaması: {description}, olan bir telegram grubumuz var. Grup yöneticisi bir mesaj yazdı: {admin_message}. '
        f'bu mesaja o grupta bulanacak bir tipte, yazım yanlışı olan ve samimi bir dilde {message_count} farklı kişi olarak yorum yapmanı istiyorum'
        'Noktalama işaretleri kullanmadan yaz ve doğal bir üslup olsun (örneğin takipteyiz harika vb) ayrıca gelecek vaadeden mesaj olmasın(örneğin bende birşeyler soracağım, hemen yazıyorum vb.). '
        f'json çıktı formatı: {json_text}'
    )
    print(system_message)
    text = re.sub(r'\s+', ' ', system_message).strip()
    
    if not text:
        return '[]'
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Veya kullanmak istediğiniz başka bir model
            messages=[{"role": "user", "content": text}],
            max_tokens=500,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # OpenAI'den gelen cevabın 'content' kısmı temizlenip JSON formatına dönüştürülüyor
        output = response.choices[0].message['content']
        # Metni JSON formatına dönüştür
        try:
            # JSON formatında olmayan kısmı temizle (örneğin extradan gelen yazılar vs.)
            json_output = re.search(r'\{.*\}', output)
            if json_output:
                return json.loads(json_output.group(0))  # JSON formatında döndür
            else:
                return None  # Geçerli JSON formatı yoksa None döndür
        except json.JSONDecodeError:
            print("JSON formatı hatalı")
            return None
    except openai.error.APIError as e:
        print(f"API Error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Yöneticilerin mesajlarını ekrana yazdıracak asenkron fonksiyon
async def main():
    # Hesaplar için client'lar oluştur
    clients = []
    for account in accounts:
        client = TelegramClient(account['phone'], account['api_id'], account['api_hash'])
        await client.start(account['phone'])
        clients.append(client)

    # Gruba katıl ve yöneticileri al
    group = await clients[0].get_entity(group_link)  # Grup nesnesini al
    admins = await clients[0].get_participants(group, filter=ChannelParticipantsAdmins)
    
    # Yöneticilerin mesajlarını takip et
    @clients[0].on(events.NewMessage(chats=group))
    async def handler(event):
        if event.sender_id in [admin.id for admin in admins] and admin_icon in event.text:
            print(f"Yönetici mesajı: {event.sender_id} - {event.text} {len(accounts)}")
            
            # Yöneticiler mesaj attığında OpenAI ile yorum al
            response_dict = analyze_text(group.title, event.text, len(accounts))
            if response_dict:
                # JSON formatında yorumları döndür
                messages_list = list(response_dict.values())  # Yorumları listeye al
                indices = list(range(len(clients)))  # Hesap indekslerini oluştur
                random.shuffle(indices)  # Hesap sırasını karıştır
                
                # Rastgeleleşmiş sıraya göre mesaj gönder
                for idx, message in zip(indices, messages_list):
                    random_delay = random.randint(1, 60)  # 1-5 saniye rastgele gecikme
                    print(f"Mesaj gönderiliyor: {message} (Hesap {idx+1}) (Bekleniyor: {random_delay} saniye)")
                    
                    # Belirtilen süre kadar bekle
                    await asyncio.sleep(random_delay)
                    
                    # Rastgele seçilen hesabı kullanarak mesaj gönder
                    await clients[idx].send_message(group.id, message)

    print("Yöneticilerin mesajları takip ediliyor...")

    # Bütün hesapları çalışır durumda tutmak için
    await asyncio.gather(*[client.run_until_disconnected() for client in clients])

# Asenkron fonksiyonu çalıştırın
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
