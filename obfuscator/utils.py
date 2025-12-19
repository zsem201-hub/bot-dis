import random
import string
import hashlib
import time

class Utils:
    """Utility functions untuk obfuscator"""
    
    # Character sets untuk random names
    CONFUSING_CHARS = "Il1O0QqUuVvWwXxYyZz"
    INVISIBLE_CHARS = ['\u200b', '\u200c', '\u200d', '\u2060', '\u2062']
    
    @staticmethod
    def random_name(length: int = 12, prefix: str = "_") -> str:
        """Generate random variable name yang susah dibaca"""
        chars = Utils.CONFUSING_CHARS + string.digits
        first = random.choice(string.ascii_letters + "_")
        rest = ''.join(random.choices(chars, k=length-1))
        return prefix + first + rest
    
    @staticmethod
    def random_hex_name(length: int = 16) -> str:
        """Generate hex-like name"""
        return '_0x' + ''.join(random.choices('0123456789abcdef', k=length))
    
    @staticmethod
    def generate_key(length: int = 32) -> str:
        """Generate random encryption key"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_numeric_key(length: int = 16) -> list:
        """Generate numeric key array"""
        return [random.randint(0, 255) for _ in range(length)]
    
    @staticmethod
    def xor_encrypt(data: str, key: str) -> list:
        """XOR encrypt string"""
        result = []
        key_len = len(key)
        for i, char in enumerate(data):
            result.append(ord(char) ^ ord(key[i % key_len]))
        return result
    
    @staticmethod
    def generate_watermark() -> str:
        """Generate unique watermark"""
        timestamp = str(time.time())
        random_str = ''.join(random.choices('abcdef0123456789', k=8))
        data = f"{timestamp}-{random_str}"
        return hashlib.sha256(data.encode()).hexdigest()[:16].upper()
    
    @staticmethod
    def to_lua_table(data: list) -> str:
        """Convert Python list ke Lua table string"""
        return "{" + ",".join(map(str, data)) + "}"
    
    @staticmethod
    def shuffle_with_map(items: list) -> tuple:
        """Shuffle list dan return mapping"""
        indexed = list(enumerate(items))
        random.shuffle(indexed)
        shuffled = [item for _, item in indexed]
        mapping = [i for i, _ in indexed]
        return shuffled, mapping
