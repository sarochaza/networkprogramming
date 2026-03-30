#token.py
import time
from config import TOKEN_EXPIRY

class Token:
    def __init__(self, message):
        self.message = message
        self.read = False
        self.timestamp = time.time()

    def read_token(self):
        # อ่านได้ครั้งเดียว + มีอายุ
        if self.read:
            return None

        if time.time() - self.timestamp > TOKEN_EXPIRY:
            return None

        self.read = True
        return self.message

