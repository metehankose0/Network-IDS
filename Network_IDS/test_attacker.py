import argparse
import time
import socket
import logging
import sys
import threading

# Configure logging properly for test script
logger = logging.getLogger("TestAttacker")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def send_syn(target_ip, target_port):
    try:
        # Standart bir TCP soketi oluşturuyoruz
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1) # Çok kısa zaman aşımı
        # connect() çağrısı işletim sistemine otomatik olarak hedefe bir "SYN" paketi göndertir
        s.connect((target_ip, target_port)) 
    except Exception:
        pass
    finally:
        s.close()
        
def syn_flood(target_ip, target_port, packet_count):
    logger.info(f"SYN Flood Testi Başlatılıyor: Hedef {target_ip}:{target_port} ...")
    logger.info(f"Gönderilecek Paket Sayısı: {packet_count}")
    
    threads = []
    # Hedefe seri bir şekilde bağlanma isteği gönderiyoruz (SYN)
    for i in range(packet_count):
        t = threading.Thread(target=send_syn, args=(target_ip, target_port))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    logger.info("Test tamamlandı. Lütfen çalışan IDS (main.py) ekranındaki uyarıları kontrol edin.")

def main():
    parser = argparse.ArgumentParser(description="IDS Test Aracı (Sadece Kendi Ağınızda Kullanın!)")
    parser.add_argument("-t", "--target", help="Saldırılacak Hedef IP (Örn: Sanal makinenizin IPsini veya kendi bilgisayarınızın yerel IP'sini yazın).", required=True)
    parser.add_argument("-p", "--port", type=int, help="Hedef Port numarası (Örn: 80)", default=80)
    parser.add_argument("-c", "--count", type=int, help="Gönderilecek SYN paket sayısı.", default=30)
    
    args = parser.parse_args()
    syn_flood(target_ip=args.target, target_port=args.port, packet_count=args.count)

if __name__ == "__main__":
    main()
