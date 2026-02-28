# 🛡️Ağ Trafiği Analizörü ve IDS (Saldırı Tespit Sistemi)

Bu proje, bir ağ cihazı ağındaki trafiği (pcap pakedi seviyesinde) gerçek zamanlı olarak dinleyerek şüpheli hareketleri ve ağ anormalliklerini tespit eden; modüler ve genişletilebilir bir Güvenlik Operasyonları (SOC) aracıdır. 

Siber güvenlik analizlerinin temelini oluşturan paket analizi tekniklerini pratik etmek ve Python ile ağ mühendisliği (Network Engineering) becerilerini geliştirmek amacıyla tasarlanmıştır.

## 🚀 Projenin Amacı
Bu projede amacım ezbere çalışan araçlar kullanmak yerine, TCP/IP protokollerine, OSI ağ modeline (Katman 3 / Ağ, Katman 4 / İletim) doğrudan erişim sağlayarak trafiği manipüle etmek ve ağ güvenliği hakkında derinlemesine bilgi sahibi olmaktır.

* **Paket Analizi:** `Scapy` modülü ile her bir paketin başlık (Header) değerleri okundu ve filtrelendi.
* **TCP Flags Okuması:** TCP bağlantısının ilk adımı olan "SYN (Synchronization)" bayraklarının anormalliği test edildi.
* **Kural Motoru Mimarisi:** İleride daha fazla saldırı türü eklenebilsin diye nesne yönelimli (OOP) yapıda şablon bir "BaseRule" sınıfı kurgulandı ve motor bu kurallarla beslendi.
* **Soket Programlama:** Ağ sınırlarını aşarak işletim sistemi düzeyindeki standart `socket` (Soket) modülü ile istemci (test saldırganı) simüle edildi.

## ✨ Özellikler
* **Gerçek Zamanlı Trafik İzleme:** Herhangi bir ağ arayüzünü (Wi-Fi, Ethernet) dinleyebilir.
* **SYN Flood DDOS Tespiti:** Aynı veya sahte bir kaynaktan kısa sürede (time-window) belirlenen eşiğin (threshold) üzerinde `SYN` (bağlantı başlatma) paketi geldiğinde tespit ve uyarı mekanizmasını tetikler.
* **Akıllı Loglama:** Loglar hem konsola basılır hem de adli bilişim (forensics) incelemeleri için `alerts.log` dosyasına saat, hedef ve kaynak adresleriyle beraber temiz bir formatta kaydedilir.
* **Saldırı Simülatörü Dosyası:** IDS sistemini test etmek amaçlı multithreading yapısıyla donatılmış bir test skripti de içerir.

## 📂 Dosya Yapısı

```
Network_IDS/
├── main.py                # İstisna yakalayan Ana (Entry) Başlatıcı Script
├── requirements.txt       # scapy==2.6.1 gereksinimleri
├── test_attacker.py       # Soket tabanlı SYN testi yapan yardımcı script
├── utils/
│   └── logger.py          # Sistem loglarını utf-8 desteğiyle konsol/dosya ayırıcı formatlayıcı modül
├── core/
│   └── sniffer.py         # Scapy'nin sniff özelliği ve listelenen kural motorlarının çalıştığı kalp
└── rules/
    ├── base_rule.py       # Kuralların implemente edeceği kalıp yapı interface'ı
    └── syn_flood.py       # TCP bayraklarını sayan, zaman bazlı SYN Flood modülü
```

## 🛠️ Gereksinimler ve Kurulum
1. **Python Kurulumu:** Cihazınızda sistem yoluna (PATH) eklenmiş Python 3 kurulu olmalıdır.
2. **Paket Yöneticisi ve Kütüphaneler:** Terminalinizde proje klasöründeyseniz şunları yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
3. **Npcap Sürücüsü (Eğer Windows işletim sisteminde iseniz Zorunludur):** 
    Scapy kütüphanesinin ağ kartından ham (raw) veri çekebilmesi için Ncap gereklidir. [npcap.com/download](https://npcap.com/#download) adresinden uygulamayı indirip kurunuz. Kurulum esnasında **"Install Npcap in WinPcap API-compatible Mode"** seçeneğini *MUTLAKA* işaretleyin.

## 🚦 Nasıl Kullanılır?

⚠️ **BİLGİ:** Ağ arayüzünü (Promiscuous mode) dinlemek işletim sistemi için yetkili bir görevdir. Komut Satırınızı (CMD) her halükarda **Yönetici Olarak Başlat (Run as Administrator)** olarak açmanız gerekmektedir.

### 1. Dinleme Motorunu (IDS) Çalıştırma
Proje dizininde Yönetici (Administrator) Komut İstemi'ni açtıktan sonra, internete girmeye yetkisi olan kartınızı `--interface` belirterek yazın (Örn: WiFi, Ethernet). Aksi halde boş bırakılırsa Scapy Windows'ta Default Gateway'i bulamadığı takdirde bir şey dinlemeyecektir.

```bash
python main.py --interface "WiFi"
```

### 2. Sistemin Test Edilmesi (Zararsız Saldırı Simülasyonu)
Sistemin çalıştığını test etmek için **YENİ BİR YÖNETİCİ CMD** ekranı daha açarak `test_attacker.py` dosyasını çalıştırın. Örneğin Dış Ağdaki Google hedefine ping atıp saniyede 30 bağlantı isteği (SYN Paketi) yolluyoruz. Sizin IP adresiniz "Saldırgan" olarak IDS panelinize düşecek.

```bash
python test_attacker.py -t 8.8.8.8 -p 80 -c 30
```

> Hata/Uyarı: Saniyede çok sayıda SYN paketini başka türlü test etmeye çalıştığımızda Windows sahte (Spoofed) IP'leri çöpe attığı veya Scapy'nin broadcast fırlatma sorunundan kaçınabilmek adına SYN atıcısı saf (raw) `socket` modülü ile yazılmıştır.

---

