from scapy.all import IP, TCP
from collections import defaultdict
import time
from .base_rule import BaseRule

class SynFloodRule(BaseRule):
    def __init__(self, threshold=20, time_window=1):
        super().__init__()
        self.name = "SYN Flood Tespit Modülü"
        self.threshold = threshold
        self.time_window = time_window
        self.syn_count = defaultdict(int)
        self.last_check_time = time.time()
        self.alerted_ips = set() 

    def process_packet(self, packet, logger):
        current_time = time.time()
        
        
        if current_time - self.last_check_time > self.time_window:
            self.syn_count.clear()
            self.alerted_ips.clear()
            self.last_check_time = current_time

        if packet.haslayer(IP) and packet.haslayer(TCP):
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            tcp_flags = packet[TCP].flags
            
            
            if tcp_flags == 'S':
                self.syn_count[ip_src] += 1
                
                if self.syn_count[ip_src] > self.threshold:
                    if ip_src not in self.alerted_ips:
                        logger.warning(
                            f"[{self.name}] Olası SYN Flood! Kaynak: {ip_src}, Hedef: {ip_dst}:{packet[TCP].dport} (Saniyede {self.syn_count[ip_src]} SYN)"
                        )
                        self.alerted_ips.add(ip_src)
