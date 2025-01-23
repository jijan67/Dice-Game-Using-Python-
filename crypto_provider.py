import os
from constants import RANDOM_BYTES

class CryptoProvider:
    @staticmethod
    def generate_uniform_random(max_value: int) -> int:
        if max_value < 0:
            raise ValueError("max_value must be non-negative")
        return int.from_bytes(os.urandom(RANDOM_BYTES), 'big') % (max_value + 1)