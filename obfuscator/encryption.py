import random
import base64
import hashlib
from .utils import Utils

class EncryptionEngine:
    """
    Advanced encryption untuk strings dan bytecode
    - Multi-layer XOR encryption
    - Dynamic key generation
    - Base64 dengan custom alphabet
    - Bytecode encryption
    """
    
    def __init__(self):
        self.utils = Utils()
        self.master_key = Utils.generate_key(32)
        self.string_cache = {}
    
    def generate_dynamic_key(self, seed: str = None) -> str:
        """Generate dynamic key berdasarkan seed"""
        if seed:
            random.seed(hashlib.md5(seed.encode()).hexdigest())
        key = Utils.generate_key(32)
        random.seed()  # Reset seed
        return key
    
    def multi_layer_xor(self, data: str, layers: int = 3) -> tuple:
        """Multi-layer XOR encryption dengan multiple keys"""
        keys = []
        encrypted = [ord(c) for c in data]
        
        for _ in range(layers):
            key = Utils.generate_key(16)
            keys.append(key)
            new_encrypted = []
            for i, byte in enumerate(encrypted):
                new_encrypted.append(byte ^ ord(key[i % len(key)]))
            encrypted = new_encrypted
        
        return encrypted, keys
    
    def generate_string_decryptor(self, var_name: str, keys: list) -> str:
        """Generate Lua function untuk decrypt string"""
        keys_table = []
        for key in reversed(keys):
            key_bytes = [ord(c) for c in key]
            keys_table.append(Utils.to_lua_table(key_bytes))
        
        decryptor_name = Utils.random_name()
        
        return f'''
local {decryptor_name} = (function()
    local keys = {{{','.join(keys_table)}}}
    return function(encrypted)
        local result = encrypted
        for i = 1, #keys do
            local key = keys[i]
            local decrypted = {{}}
            for j = 1, #result do
                local keyIndex = ((j - 1) % #key) + 1
                decrypted[j] = bit32 and bit32.bxor(result[j], key[keyIndex]) or 
                    (function(a, b)
                        local r = 0
                        for k = 0, 7 do
                            local ba, bb = a % 2, b % 2
                            if ba ~= bb then r = r + 2^k end
                            a, b = math.floor(a/2), math.floor(b/2)
                        end
                        return r
                    end)(result[j], key[keyIndex])
            end
            result = decrypted
        end
        local str = ""
        for i = 1, #result do
            str = str .. string.char(result[i])
        end
        return str
    end
end)()
'''
    
    def encrypt_string(self, s: str, complexity: int = 3) -> tuple:
        """Encrypt single string dengan multiple layers"""
        if s in self.string_cache:
            return self.string_cache[s]
        
        encrypted, keys = self.multi_layer_xor(s, complexity)
        result = (encrypted, keys)
        self.string_cache[s] = result
        return result
    
    def generate_bytecode_encryptor(self) -> tuple:
        """Generate bytecode encryption layer"""
        key = Utils.generate_numeric_key(32)
        key_name = Utils.random_name()
        decrypt_func = Utils.random_name()
        
        key_table = Utils.to_lua_table(key)
        
        encryptor_code = f'''
local {key_name} = {key_table}
local {decrypt_func} = function(data)
    local result = {{}}
    for i = 1, #data do
        local keyIndex = ((i - 1) % #{key_name}) + 1
        local decrypted = bit32 and bit32.bxor(data[i], {key_name}[keyIndex]) or
            (function(a, b)
                local r = 0
                for k = 0, 7 do
                    local ba, bb = a % 2, b % 2
                    if ba ~= bb then r = r + 2^k end
                    a, b = math.floor(a/2), math.floor(b/2)
                end
                return r
            end)(data[i], {key_name}[keyIndex])
        result[i] = decrypted
    end
    local str = ""
    for i = 1, #result do
        str = str .. string.char(result[i])
    end
    return str
end
'''
        return encryptor_code, decrypt_func, key
    
    def create_base64_decoder(self, custom_alphabet: bool = True) -> tuple:
        """Create base64 decoder dengan optional custom alphabet"""
        func_name = Utils.random_name()
        
        if custom_alphabet:
            # Shuffle base64 alphabet
            alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")
            random.shuffle(alphabet)
            alphabet_str = ''.join(alphabet)
        else:
            alphabet_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        
        decoder_code = f'''
local {func_name} = (function()
    local alphabet = "{alphabet_str}"
    return function(data)
        local result = ""
        local buffer = 0
        local bits = 0
        for i = 1, #data do
            local char = data:sub(i, i)
            local index = alphabet:find(char)
            if index then
                buffer = buffer * 64 + (index - 1)
                bits = bits + 6
                while bits >= 8 do
                    bits = bits - 8
                    result = result .. string.char(math.floor(buffer / 2^bits) % 256)
                end
            end
        end
        return result
    end
end)()
'''
        return decoder_code, func_name, alphabet_str
    
    def encode_with_custom_base64(self, data: str, alphabet: str) -> str:
        """Encode data dengan custom base64 alphabet"""
        standard = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        encoded = base64.b64encode(data.encode()).decode()
        
        # Replace dengan custom alphabet
        result = ""
        for char in encoded:
            if char in standard:
                result += alphabet[standard.index(char)]
            else:
                result += char
        return result
