import random
import re
import base64

class ObfuscationLayers:
    """Multiple obfuscation layers"""
    
    def __init__(self):
        self.string_map = {}
        self.var_counter = 0
    
    def random_name(self, length=10):
        chars = "Il1O0"
        first = "_"
        return first + ''.join(random.choices(chars, k=length))
    
    # ===== LAYER 1: String Encryption =====
    def encrypt_strings(self, code: str) -> str:
        """Encrypt semua string literals"""
        string_table_name = self.random_name()
        strings = []
        
        def replace_string(match):
            s = match.group(1) or match.group(2)
            if s not in self.string_map:
                idx = len(strings)
                # XOR encrypt
                key = random.randint(1, 255)
                encrypted = [ord(c) ^ key for c in s]
                strings.append((encrypted, key))
                self.string_map[s] = idx
            return f'{string_table_name}[{self.string_map[s]}]'
        
        # Match strings
        pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\'\\]*(?:\\.[^\'\\]*)*)\''
        code = re.sub(pattern, replace_string, code)
        
        # Build string table
        table_entries = []
        for encrypted, key in strings:
            bytes_str = "{" + ",".join(map(str, encrypted)) + "}"
            table_entries.append(f'(function()local t={bytes_str} local r="" for i=1,#t do r=r..string.char(t[i]~{key})end return r end)()')
        
        if strings:
            string_table = f'local {string_table_name}={{{",".join(table_entries)}}}\n'
            return string_table + code
        return code
    
    # ===== LAYER 2: Variable Renaming =====
    def rename_variables(self, code: str) -> str:
        """Rename semua local variables"""
        # Simple pattern untuk local variables
        var_map = {}
        
        def get_new_name(old_name):
            if old_name not in var_map:
                var_map[old_name] = self.random_name()
            return var_map[old_name]
        
        # Find and replace local variable declarations
        def replace_local(match):
            var_name = match.group(1)
            if var_name not in ['if', 'then', 'else', 'end', 'function', 'local', 'return', 'for', 'while', 'do', 'in', 'and', 'or', 'not', 'true', 'false', 'nil']:
                return f'local {get_new_name(var_name)}'
            return match.group(0)
        
        code = re.sub(r'local\s+([a-zA-Z_][a-zA-Z0-9_]*)', replace_local, code)
        
        # Replace usages
        for old_name, new_name in var_map.items():
            code = re.sub(rf'\b{old_name}\b', new_name, code)
        
        return code
    
    # ===== LAYER 3: Control Flow Obfuscation =====
    def obfuscate_control_flow(self, code: str) -> str:
        """Add fake control flow"""
        opaque_var = self.random_name()
        dead_code = self.random_name()
        
        # Add opaque predicate
        prefix = f'''
local {opaque_var} = (function()
    local a = math.floor(os.clock() * 1000) % 1000
    return a >= 0
end)()

local function {dead_code}()
    local x = {{}}
    for i = 1, math.random(1, 10) do
        x[i] = string.char(math.random(65, 90))
    end
    return table.concat(x)
end

if not {opaque_var} then
    {dead_code}()
    return
end

'''
        return prefix + code
    
    # ===== LAYER 4: Number Encoding =====
    def encode_numbers(self, code: str) -> str:
        """Encode number literals"""
        def encode_num(match):
            num = int(match.group(0))
            # Random encoding method
            method = random.randint(1, 3)
            if method == 1:
                # XOR encoding
                key = random.randint(1, 1000)
                encoded = num ^ key
                return f'({encoded}~{key})'  # Lua 5.3+ XOR
            elif method == 2:
                # Math expression
                a = random.randint(1, 100)
                b = num - a
                return f'({a}+{b})'
            else:
                # Bit shift (if applicable)
                return str(num)
        
        # Only encode standalone numbers, not in variable names
        code = re.sub(r'(?<![a-zA-Z_])\b(\d+)\b(?![a-zA-Z_])', encode_num, code)
        return code
    
    # ===== LAYER 5: Add Junk Code =====
    def add_junk_code(self, code: str, intensity: int = 5) -> str:
        """Insert junk/dead code"""
        junk_templates = [
            'local {v} = function() return nil end',
            'local {v} = {{}};{v}[1] = {v}',
            'local {v} = tostring(math.random())',
            '(function() local {v} = 0 end)()',
            'local {v} = string.rep("", 0)',
        ]
        
        lines = code.split('\n')
        new_lines = []
        
        for line in lines:
            new_lines.append(line)
            if random.random() < 0.2 and intensity > 3:  # 20% chance
                junk = random.choice(junk_templates).format(v=self.random_name())
                new_lines.append(junk)
        
        return '\n'.join(new_lines)
    
    # ===== LAYER 6: Compress & Encode =====
    def compress_and_encode(self, code: str, layers: int = 2) -> str:
        """Multi-layer base64 encoding dengan custom loader"""
        loader_name = self.random_name()
        data_name = self.random_name()
        decode_name = self.random_name()
        
        # Encode multiple layers
        encoded = code
        for _ in range(layers):
            encoded = base64.b64encode(encoded.encode()).decode()
        
        decoder = f'''
local {decode_name} = function(s)
    local b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    local r = '' local buf = 0 local bits = 0
    for i = 1, #s do
        local c = s:sub(i, i)
        local idx = b:find(c)
        if idx then
            buf = buf * 64 + (idx - 1)
            bits = bits + 6
            while bits >= 8 do
                bits = bits - 8
                r = r .. string.char(math.floor(buf / 2^bits) % 256)
            end
        end
    end
    return r
end

local {data_name} = "{encoded}"
local {loader_name} = {data_name}
'''
        
        # Add layer decoders
        for i in range(layers):
            loader_name_new = self.random_name()
            decoder += f'local {loader_name_new} = {decode_name}({loader_name})\n'
            loader_name = loader_name_new
        
        decoder += f'return (loadstring or load)({loader_name})()'
        
        return decoder
