import random
import base64
import hashlib
import struct

class LuaEncryption:
    """Advanced encryption untuk Lua strings"""
    
    @staticmethod
    def generate_key(length=32):
        return ''.join(random.choices('abcdef0123456789', k=length))
    
    @staticmethod
    def xor_encrypt(data: str, key: str) -> list:
        """XOR encryption"""
        result = []
        for i, char in enumerate(data):
            result.append(ord(char) ^ ord(key[i % len(key)]))
        return result
    
    @staticmethod
    def to_byte_array(data: str) -> str:
        """Convert string ke Lua byte array"""
        bytes_list = [str(ord(c)) for c in data]
        return "{" + ",".join(bytes_list) + "}"
    
    @staticmethod
    def base64_layers(data: str, layers: int = 3) -> str:
        """Multi-layer base64 encoding"""
        result = data
        for _ in range(layers):
            result = base64.b64encode(result.encode()).decode()
        return result
    
    @staticmethod
    def create_decoder_function(var_name: str) -> str:
        """Generate Lua base64 decoder"""
        return f'''local function {var_name}(s)
local b='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
local r=''local buf=0 local bits=0
for i=1,#s do local c=s:sub(i,i)local idx=b:find(c)
if idx then buf=buf*64+(idx-1)bits=bits+6
while bits>=8 do bits=bits-8 r=r..string.char(math.floor(buf/2^bits)%256)end end end
return r end'''
    
    @staticmethod
    def create_xor_decoder(key: str, var_name: str) -> str:
        """Generate Lua XOR decoder"""
        return f'''local function {var_name}(t,k)
local r=''k=k or"{key}"for i=1,#t do 
r=r..string.char(bit32 and bit32.bxor(t[i],k:byte((i-1)%#k+1))or 
(function(a,b)local r=0 for i=0,7 do local ba,bb=a%2,b%2 
if ba~=bb then r=r+2^i end a,b=math.floor(a/2),math.floor(b/2)end return r end)(t[i],k:byte((i-1)%#k+1)))
end return r end'''
