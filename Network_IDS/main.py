import argparse
import sys
import os

# Python'un klasör yapısını tanıması için gerekli yolu ekliyoruz
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.sniffer import NetworkSniffer
from rules.syn_flood import SynFloodRule
from utils.logger import logger

def display_banner():
    banner = r"""
     _   _      _                      _   ___  ____  ____  
    | \ | | ___| |___      _____  _ __| | |_ _|  _ \/ ___| 
    |  \| |/ _ \ __\ \ /\ / / _ \| '__| |/ /| | | | \___ \ 
    | |\  |  __/ |_ \ V  V / (_) | |  |   < | | |_| |___) |
    |_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\___|____/|____/ 
                                                           
    Basit Saldırı Tespit Sistemi (IDS) Başlatılıyor...
    ======================================================
    """
    print(banner)

def main():
    parser = argparse.ArgumentParser(description="Basit Ağ Trafiği Analizörü ve IDS")
    parser.add_argument("-i", "--interface", help="Dinlenecek ağ arayüzü (örneğin: wlan0, Ethernet). Boş bırakılırsa varsayılan dinlenir.", default=None)
    args = parser.parse_args()

    display_banner()
    
    # Kural örneklerini oluştur (Threshold değerleri yani uyarı eşikleri değiştirilebilir)
    # Örneğin: 1 saniyede aynı IP'den 15 SYN paketi gelirse uyarı ver!
    syn_flood_rule = SynFloodRule(threshold=15, time_window=1) 
    
    # Sniffer'ı ayağa kaldır
    sniffer = NetworkSniffer(interface=args.interface)
    
    # Kuralları sniffer'a ekle
    sniffer.add_rule(syn_flood_rule)
    
    # Dinlemeyi başlat
    sniffer.start()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Beklenmeyen bir hata oluştu: {e}")
