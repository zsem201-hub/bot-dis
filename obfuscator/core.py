import random
import time
import hashlib
import base64
from .utils import Utils
from .encryption import EncryptionEngine
from .virtualization import VirtualMachine
from .control_flow import ControlFlowObfuscator
from .anti_tamper import AntiTamperGenerator
from .junk_code import JunkCodeGenerator

class LuaShieldPro:
    """
    LuaShield Pro - Professional Lua Obfuscator
    Mirip dengan Luraph/Luarmor
    
    Features:
    - Virtualization (Custom VM)
    - Control Flow Flattening
    - Opaque Predicates
    - String Encryption
    - Bytecode Encryption
    - Anti-Tamper
    - HWID Lock
    - Multi-Layer Obfuscation
    - Junk Code Injection
    - Dynamic Keys
    """
    
    PRESETS = {
        'light': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': False,
            'opaque_predicates': False,
            'virtualization': False,
            'anti_tamper': False,
            'hwid_lock': False,
            'junk_code': False,
            'compression_layers': 1,
            'bytecode_encryption': False,
        },
        'medium': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': True,
            'opaque_predicates': True,
            'virtualization': False,
            'anti_tamper': True,
            'hwid_lock': False,
            'junk_code': True,
            'compression_layers': 2,
            'bytecode_encryption': False,
        },
        'standard': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': True,
            'opaque_predicates': True,
            'virtualization': False,
            'anti_tamper': True,
            'hwid_lock': False,
            'junk_code': True,
            'compression_layers': 2,
            'bytecode_encryption': True,
        },
        'maximum': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': True,
            'opaque_predicates': True,
            'virtualization': True,
            'anti_tamper': True,
            'hwid_lock': False,
            'junk_code': True,
            'compression_layers': 3,
            'bytecode_encryption': True,
        },
        'ultra': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': True,
            'opaque_predicates': True,
            'virtualization': True,
            'anti_tamper': True,
            'hwid_lock': True,
            'junk_code': True,
            'compression_layers': 4,
            'bytecode_encryption': True,
        }
    }
    
    def __init__(self):
        self.encryption = EncryptionEngine()
        self.vm = VirtualMachine()
        self.control_flow = ControlFlowObfuscator()
        self.anti_tamper = AntiTamperGenerator()
        self.junk_gen = JunkCodeGenerator()
        self.watermark = None
    
    def generate_header(self, level: str) -> str:
        """Generate header berdasarkan level"""
        
        self.watermark = Utils.generate_watermark()
        
        headers = {
            'light': f'-- LuaShield | {self.watermark}\n',
            'medium': f'''--[[
    LuaShield Pro - Protected Script
    Watermark: {self.watermark}
--]]
''',
            'standard': f'''--[[
╔═══════════════════════════════════════════════════════════╗
║  LuaShield Pro - Standard Protection                      ║
║  Watermark: {self.watermark}                          ║
║  Unauthorized copying/modification is prohibited          ║
╚═══════════════════════════════════════════════════════════╝
--]]
''',
            'maximum': f'''--[[
╔══════════════════════════════════════════════════════════════════════╗
║  ██╗     ██╗   ██╗ █████╗ ███████╗██╗  ██╗██╗███████╗██╗     ██████╗ ║
║  ██║     ██║   ██║██╔══██╗██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗║
║  ██║     ██║   ██║███████║███████╗███████║██║█████╗  ██║     ██║  ██║║
║  ██║     ██║   ██║██╔══██║╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║║
║  ███████╗╚██████╔╝██║  ██║███████║██║  ██║██║███████╗███████╗██████╔╝║
║  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝ ║
╠══════════════════════════════════════════════════════════════════════╣
║  MAXIMUM PROTECTION ENABLED                                          ║
║  ├─ Virtualization: ✓                                                ║
║  ├─ Control Flow Obfuscation: ✓                                      ║
║  ├─ String Encryption: ✓                                             ║
║  ├─ Anti-Tamper: ✓                                                   ║
║  └─ Bytecode Encryption: ✓                                           ║
╠══════════════════════════════════════════════════════════════════════╣
║  Watermark: {self.watermark}                                     ║
╚══════════════════════════════════════════════════════════════════════╝
--]]
''',
            'ultra': f'''--[[
╔══════════════════════════════════════════════════════════════════════╗
║  ██╗     ██╗   ██╗ █████╗ ███████╗██╗  ██╗██╗███████╗██╗     ██████╗ ║
║  ██║     ██║   ██║██╔══██╗██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗║
║  ██║     ██║   ██║███████║███████╗███████║██║█████╗  ██║     ██║  ██║║
║  ██║     ██║   ██║██╔══██║╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║║
║  ███████╗╚██████╔╝██║  ██║███████║██║  ██║██║███████╗███████╗██████╔╝║
║  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝ ║
╠══════════════════════════════════════════════════════════════════════╣
║  🔒 ULTRA PROTECTION - MAXIMUM SECURITY                              ║
║  ════════════════════════════════════════                            ║
║  ├─ Custom VM Execution: ✓                                           ║
║  ├─ Control Flow Flattening: ✓                                       ║
║  ├─ Opaque Predicates: ✓                                             ║
║  ├─ Multi-Layer String Encryption: ✓                                 ║
║  ├─ Bytecode Encryption: ✓                                           ║
║  ├─ Anti-Tamper Protection: ✓                                        ║
║  ├─ Anti-Debug: ✓                                                    ║
║  ├─ HWID Lock: ✓                                                     ║
║  ├─ Junk Code Injection: ✓                                           ║
║  └─ Dynamic Encryption Keys: ✓                                       ║
╠══════════════════════════════════════════════════════════════════════╣
║  Watermark: {self.watermark}                                     ║
║  Protected by LuaShield Pro | DO NOT REDISTRIBUTE                    ║
╚══════════════════════════════════════════════════════════════════════╝
--]]
'''
        }
        
        return headers.get(level, headers['standard'])
    
    def obfuscate(self, code: str, level: str = 'standard', 
                  hwid_list: list = None, custom_config: dict = None) -> tuple:
        """
        Main obfuscation method
        
        Args:
            code: Source Lua code
            level: Protection level (light/medium/standard/maximum/ultra)
            hwid_list: List of allowed HWIDs (optional)
            custom_config: Custom configuration (optional)
        
        Returns:
            tuple: (obfuscated_code, stats_dict)
        """
        
        start_time = time.time()
        original_size = len(code)
        
        # Get configuration
        if level not in self.PRESETS:
            level = 'standard'
        
        config = self.PRESETS[level].copy()
        if custom_config:
            config.update(custom_config)
        
        if hwid_list:
            config['hwid_lock'] = True
        
        result = code
        layers_applied = []
        
        try:
            # Generate header
            header = self.generate_header(level)
            
            # Layer 1: String Encryption
            if config['string_encryption']:
                result = self._apply_string_encryption(result)
                layers_applied.append('String Encryption')
            
            # Layer 2: Variable Renaming (basic)
            if config['variable_rename']:
                result = self._apply_variable_rename(result)
                layers_applied.append('Variable Renaming')
            
            # Layer 3: Opaque Predicates
            if config['opaque_predicates']:
                result = self.control_flow.add_opaque_branches(result)
                layers_applied.append('Opaque Predicates')
            
            # Layer 4: Junk Code
            if config['junk_code']:
                intensity = 5 if level in ['maximum', 'ultra'] else 3
                result = self.junk_gen.inject_junk_code(result, intensity)
                layers_applied.append('Junk Code')
            
            # Layer 5: Control Flow
            if config['control_flow']:
                # Add control flow elements
                prefix = f'''
-- Control Flow Protection
{self.control_flow.generate_opaque_predicate(True)} or (function() end)()
{self.control_flow.generate_fake_loops()}
'''
                result = prefix + result
                layers_applied.append('Control Flow')
            
            # Layer 6: Anti-Tamper
            if config['anti_tamper']:
                code_hash = hashlib.sha256(result.encode()).hexdigest()[:16]
                anti_tamper_code = self.anti_tamper.generate_full_protection(
                    code_hash, 
                    hwid_list if config['hwid_lock'] else None
                )
                result = anti_tamper_code + '\n' + result
                layers_applied.append('Anti-Tamper')
                if config['hwid_lock'] and hwid_list:
                    layers_applied.append('HWID Lock')
            
            # Layer 7: Bytecode Encryption
            if config['bytecode_encryption']:
                result = self._apply_bytecode_encryption(result, config['compression_layers'])
                layers_applied.append(f'Bytecode Encryption ({config["compression_layers"]}x)')
            
            # Layer 8: Virtualization
            if config['virtualization']:
                result = self.vm.generate_vm_wrapper(result)
                layers_applied.append('VM Virtualization')
            
            # Add header
            result = header + result
            
        except Exception as e:
            raise Exception(f"Obfuscation failed: {str(e)}")
        
        # Calculate stats
        end_time = time.time()
        
        stats = {
            'original_size': original_size,
            'obfuscated_size': len(result),
            'size_ratio': f"{(len(result) / original_size * 100):.1f}%",
            'level': level.upper(),
            'watermark': self.watermark,
            'layers_applied': layers_applied,
            'layers_count': len(layers_applied),
            'processing_time': f"{(end_time - start_time) * 1000:.2f}ms",
            'protection_score': self._calculate_score(config)
        }
        
        return result, stats
    
    def _apply_string_encryption(self, code: str) -> str:
        """Apply string encryption"""
        import re
        
        string_table = Utils.random_name()
        decrypt_func = Utils.random_name()
        strings = []
        
        def replace_string(match):
            s = match.group(1) or match.group(2)
            if not s or len(s) == 0:
                return match.group(0)
            
            # Encrypt string
            key = Utils.generate_key(8)
            encrypted = Utils.xor_encrypt(s, key)
            
            idx = len(strings)
            strings.append((encrypted, key))
            return f'{string_table}[{idx + 1}]'
        
        # Find and replace strings
        pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\'\\]*(?:\\.[^\'\\]*)*)\''
        code = re.sub(pattern, replace_string, code)
        
        if not strings:
            return code
        
        # Build decryption table
        entries = []
        for encrypted, key in strings:
            enc_str = Utils.to_lua_table(encrypted)
            key_bytes = Utils.to_lua_table([ord(c) for c in key])
            entries.append(f'''(function()
    local e = {enc_str}
    local k = {key_bytes}
    local r = ""
    for i = 1, #e do
        local ki = ((i - 1) % #k) + 1
        r = r .. string.char(bit32 and bit32.bxor(e[i], k[ki]) or 
            (function(a, b)
                local x = 0
                for j = 0, 7 do
                    local ba, bb = a % 2, b % 2
                    if ba ~= bb then x = x + 2^j end
                    a, b = math.floor(a/2), math.floor(b/2)
                end
                return x
            end)(e[i], k[ki]))
    end
    return r
end)()''')
        
        table_code = f'local {string_table} = {{{",".join(entries)}}}\n\n'
        return table_code + code
    
    def _apply_variable_rename(self, code: str) -> str:
        """Basic variable renaming"""
        import re
        
        var_map = {}
        counter = [0]
        
        def get_new_name(name):
            if name not in var_map:
                var_map[name] = Utils.random_name()
                counter[0] += 1
            return var_map[name]
        
        # Rename local variables
        keywords = {'if', 'then', 'else', 'elseif', 'end', 'function', 'local', 
                   'return', 'for', 'while', 'do', 'in', 'and', 'or', 'not',
                   'true', 'false', 'nil', 'break', 'repeat', 'until', 'goto'}
        
        def replace_local(match):
            name = match.group(1)
            if name in keywords:
                return match.group(0)
            return f'local {get_new_name(name)}'
        
        code = re.sub(r'local\s+([a-zA-Z_][a-zA-Z0-9_]*)', replace_local, code)
        
        # Replace usages
        for old_name, new_name in var_map.items():
            code = re.sub(rf'\b{re.escape(old_name)}\b', new_name, code)
        
        return code
    
    def _apply_bytecode_encryption(self, code: str, layers: int = 2) -> str:
        """Apply multi-layer bytecode encryption"""
        
        # Create base64 decoder
        decoder_code, decoder_func, alphabet = self.encryption.create_base64_decoder(True)
        
        # Encode with custom alphabet
        encoded = code
        for _ in range(layers):
            encoded = self.encryption.encode_with_custom_base64(encoded, alphabet)
        
        # Generate loader
        data_var = Utils.random_name()
        temp_vars = [Utils.random_name() for _ in range(layers)]
        
        loader = decoder_code + '\n'
        loader += f'local {data_var} = "{encoded}"\n'
        
        # Add decode layers
        prev_var = data_var
        for i, temp_var in enumerate(temp_vars):
            loader += f'local {temp_var} = {decoder_func}({prev_var})\n'
            prev_var = temp_var
        
        # Execute
        exec_var = Utils.random_name()
        loader += f'''
local {exec_var} = (loadstring or load)({prev_var})
if {exec_var} then
    {exec_var}()
end
'''
        
        return loader
    
    def _calculate_score(self, config: dict) -> str:
        """Calculate protection score"""
        score = 0
        
        if config['string_encryption']: score += 10
        if config['variable_rename']: score += 10
        if config['control_flow']: score += 15
        if config['opaque_predicates']: score += 10
        if config['virtualization']: score += 25
        if config['anti_tamper']: score += 15
        if config['hwid_lock']: score += 10
        if config['junk_code']: score += 5
        if config['bytecode_encryption']: score += 10
        score += config['compression_layers'] * 2
        
        stars = min(5, score // 20)
        return f"{score}/100 {'⭐' * stars}"
