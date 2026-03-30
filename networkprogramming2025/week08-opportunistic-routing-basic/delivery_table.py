#delivery_table.py
class DeliveryTable:
    def __init__(self):
        self.table = {}  # {peer_port: probability}

    def update_probability(self, peer, prob):
        self.table[peer] = prob

    def get_probability(self, peer):
        return self.table.get(peer, 0.0)

    def get_best_candidates(self, threshold):
        return [peer for peer, prob in self.table.items() if prob >= threshold]

        