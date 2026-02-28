from scapy.all import sniff
from utils.logger import logger

class NetworkSniffer:
    def __init__(self, interface=None):
        self.interface = interface
        self.rules = []
        
    def add_rule(self, rule):
        self.rules.append(rule)
        logger.info(f"Kural sisteme eklendi: {rule.name}")

    def _packet_handler(self, packet):
        # Her gelen paketi kural motorlarına gönderir
        for rule in self.rules:
            try:
                rule.process_packet(packet, logger)
            except Exception as e:
                logger.error(f"Paket analiz hatası ({rule.name}): {e}")

    def start(self):
        logger.info(f"Ağ dinleniyor... (Arayüz: {self.interface if self.interface else 'Varsayılan'}). Çıkış için Ctrl+C'ye basın.")
        try:
            # scapy sniff fonksiyonunu çağırır
            # store=0 belleğin dolmasını önler (yakalanan paketleri RAM'de biriktirmez)
            sniff(iface=self.interface, prn=self._packet_handler, store=0)
        except KeyboardInterrupt:
            logger.info("Ağ dinleme kullanıcı tarafından durduruldu.")
        except Exception as e:
            logger.error(f"Sniffer motoru başlatılamadı veya durdu: {e}")
