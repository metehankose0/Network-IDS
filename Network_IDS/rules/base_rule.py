class BaseRule:
    def __init__(self):
        self.name = "Base Rule"
        
    def process_packet(self, packet, logger):
        """
        Gelen paketi analiz eder. Her kural kendi analiz kodunu bura yazmalıdır.
        """
        raise NotImplementedError("process_packet metodu uygulanmalıdır.")
