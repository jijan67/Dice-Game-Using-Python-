import os
import hmac
import hashlib
from typing import Tuple
from crypto_provider import CryptoProvider
from constants import KEY_SIZE_BYTES

class FairNumberGenerator:
    def __init__(self, crypto_provider: CryptoProvider):
        self.crypto_provider = crypto_provider

    def generate_fair_number(self, max_value: int) -> Tuple[int, bytes, str]:
        key = os.urandom(KEY_SIZE_BYTES)
        number = self.crypto_provider.generate_uniform_random(max_value)
        hmac_value = hmac.new(key, str(number).encode(), hashlib.sha256).hexdigest()
        return number, key, hmac_value