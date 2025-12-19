import random
import time
import hashlib
import base64
import re
from .utils import Utils
from .encryption import EncryptionEngine
from .vm_generator import VirtualMachine
from .anti_tamper import AntiTamperGenerator
from .junk_code import JunkCodeGenerator

class LuaShieldPro:
    """
    LuaShield Pro v2.1 - With Custom Mode
    Optimized for Roblox Executors (Delta, Fluxus, etc.)
    """
    
    # Preset levels
    PRESETS = {
        'light': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': False,
            'junk_code': False,
            'junk_intensity': 0,
            'anti_tamper': False,
            'anti_debug': False,
            'virtualization': False,
            'compression_layers': 1,
            'hwid_lock': False,
            'minify': True,
            'watermark_hidden': True,
        },
        'medium': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': True,
            'junk_code': True,
            'junk_intensity': 2,
            'anti_tamper': True,
            'anti_debug': False,
            'virtualization': False,
            'compression_layers': 2,
            'hwid_lock': False,
            'minify': True,
            'watermark_hidden': True,
        },
        'standard': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': True,
            'junk_code': True,
            'junk_intensity': 3,
            'anti_tamper': True,
            'anti_debug': True,
            'virtualization': False,
            'compression_layers': 2,
            'hwid_lock': False,
            'minify': True,
            'watermark_hidden': True,
        },
        'maximum': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': True,
            'junk_code': True,
            'junk_intensity': 4,
            'anti_tamper': True,
            'anti_debug': True,
            'virtualization': True,
            'compression_layers': 3,
            'hwid_lock': False,
            'minify': True,
            'watermark_hidden': True,
        },
        'ultra': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': True,
            'junk_code': True,
            'junk_intensity': 5,
            'anti_tamper': True,
            'anti_debug': True,
            'virtualization': True,
            'compression_layers': 4,
            'hwid_lock': True,
            'minify': True,
            'watermark_hidden': True,
        },
        # Optimized presets untuk executor yang lemah
        'delta': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': False,
            'junk_code': False,
            'junk_intensity': 0,
            'anti_tamper': True,
            'anti_debug': False,
            'virtualization': False,
            'compression_layers': 1,
            'hwid_lock': False,
            'minify': True,
            'watermark_hidden': True,
        },
        'mobile': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': False,
            'junk_code': False,
            'junk_intensity': 0,
            'anti_tamper': False,
            'anti_debug': False,
            'virtualization': False,
            'compression_layers': 1,
            'hwid_lock': False,
            'minify': True,
            'watermark_hidden': True,
        },
        'balanced': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': True,
            'junk_code': False,
            'junk_intensity': 0,
            'anti_tamper': True,
            'anti_debug': False,
            'virtualization': False,
            'compression_layers': 2,
            'hwid_lock': False,
            'minify': True,
            'watermark_hidden': True,
        },
    }
    
    # Feature descriptions
    FEATURES = {
        'string_encryption': {
            'name': 'String Encryption',
            'emoji': '🔐',
            'desc': 'Encrypt all string literals',
            'impact': 'low',  # CPU impact
            'size': 'medium',  # Size increase
        },
        'variable_rename': {
            'name': 'Variable Rename',
            'emoji': '📝',
            'desc': 'Rename variables to unreadable names',
            'impact': 'none',
            'size': 'none',
        },
        'control_flow': {
            'name': 'Control Flow',
            'emoji': '🔀',
            'desc': 'Add opaque predicates',
            'impact': 'low',
            'size': 'low',
        },
        'junk_code': {
            'name': 'Junk Code',
            'emoji': '🗑️',
            'desc': 'Insert dead code',
            'impact': 'medium',
            'size': 'high',
        },
        'anti_tamper': {
            'name': 'Anti-Tamper',
            'emoji': '🛡️',
            'desc': 'Integrity checks',
            'impact': 'low',
            'size': 'medium',
        },
        'anti_debug': {
            'name': 'Anti-Debug',
            'emoji': '🚫',
            'desc': 'Detect debugging',
            'impact': 'low',
            'size': 'low',
        },
        'virtualization': {
            'name': 'VM Protection',
            'emoji': '🖥️',
            'desc': 'Custom VM wrapper',
            'impact': 'high',
            'size': 'high',
        },
        'hwid_lock': {
            'name': 'HWID Lock',
            'emoji': '🔑',
            'desc': 'Lock to specific devices',
            'impact': 'low',
            'size': 'low',
        },
        'minify': {
            'name': 'Minify',
            'emoji': '📦',
            'desc': 'Remove whitespace',
            'impact': 'none',
            'size': 'negative',  # Reduces size
        },
    }
    
    def __init__(self):
        self.encryption = EncryptionEngine()
        self.vm = VirtualMachine()
        self.anti_tamper = AntiTamperGenerator()
        self.junk = JunkCodeGenerator()
        self.watermark = None
    
    @classmethod
    def get_default_config(cls) -> dict:
        """Get default configuration (all off)"""
        return {
            'string_encryption': False,
            'variable_rename': False,
            'control_flow': False,
            'junk_code': False,
            'junk_intensity': 0,
            'anti_tamper': False,
            'anti_debug': False,
            'virtualization': False,
            'compression_layers': 1,
            'hwid_lock': False,
            'minify': False,
            'watermark_hidden': True,
        }
    
    @classmethod
    def get_feature_list(cls) -> list:
        """Get list of toggleable features"""
        return [
            'string_encryption',
            'variable_rename', 
            'control_flow',
            'junk_code',
            'anti_tamper',
            'anti_debug',
            'virtualization',
            'hwid_lock',
            'minify',
        ]
    
    def _generate_header(self, hidden: bool = True) -> str:
        """Generate watermark header"""
        self.watermark = Utils.generate_watermark()
        
        if hidden:
            # Invisible watermark
            return f'--[[{self.watermark}]]'
        return f'--LS|{self.watermark}'
    
    def _extract_strings(self, code: str) -> tuple:
        """Extract string literals"""
        strings = []
        placeholder = Utils.random_var()
        
        def replace_string(match):
            s = match.group(1) or match.group(2)
            if s and len(s) > 0:
                idx = len(strings)
                strings.append(s)
                return f'{placeholder}[{idx + 1}]'
            return match.group(0)
        
        pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\'\\]*(?:\\.[^\'\\]*)*)\''
        new_code = re.sub(pattern, replace_string, code)
        
        return new_code, strings, placeholder
    
    def _encrypt_strings_optimized(self, code: str) -> str:
        """Optimized string encryption - lighter version"""
        new_code, strings, placeholder = self._extract_strings(code)
        
        if not strings:
            return code
        
        # Generate simple XOR key
        key = Utils.generate_numeric_key(8)  # Shorter key
        key_str = Utils.to_lua_array(key)
        
        # Simple XOR function (optimized)
        xor_var = Utils.random_var()
        table_var = Utils.random_var()
        
        xor_func = f'''local {xor_var}=function(e,k)local r=""for i=1,#e do r=r..string.char(e[i]~k[(i-1)%#k+1])end return r end
'''
        
        # Encrypt strings
        entries = []
        for s in strings:
            encrypted = []
            for i, char in enumerate(s):
                encrypted.append(ord(char) ^ key[i % len(key)])
            enc_str = Utils.to_lua_array(encrypted)
            entries.append(f'{xor_var}({enc_str},{key_str})')
        
        table_code = f'{xor_func}local {table_var}={{{",".join(entries)}}}\n'
        
        return table_code + new_code.replace(placeholder, table_var)
    
    def _rename_variables(self, code: str) -> str:
        """Rename local variables"""
        var_map = {}
        
        # Lua + Roblox keywords
        keywords = {
            'if', 'then', 'else', 'elseif', 'end', 'function', 'local',
            'return', 'for', 'while', 'do', 'in', 'and', 'or', 'not',
            'true', 'false', 'nil', 'break', 'repeat', 'until', 'goto',
            'self', 'pairs', 'ipairs', 'next', 'select', 'unpack', 'table',
            'string', 'math', 'coroutine', 'debug', 'io', 'os', 'print',
            'type', 'tostring', 'tonumber', 'error', 'pcall', 'xpcall',
            'rawget', 'rawset', 'setmetatable', 'getmetatable', 'require',
            'loadstring', 'load', 'loadfile', 'dofile', 'assert',
            'game', 'workspace', 'script', 'Instance', 'Vector3', 'CFrame',
            'Color3', 'BrickColor', 'Enum', 'UDim2', 'UDim', 'Ray', 'Region3',
            'wait', 'spawn', 'delay', 'tick', 'time', 'typeof', 'warn',
            'shared', '_G', 'getfenv', 'setfenv', 'collectgarbage',
            'Players', 'Workspace', 'ReplicatedStorage', 'ServerStorage',
            'LocalPlayer', 'Character', 'Humanoid', 'HumanoidRootPart',
        }
        
        def get_new_name(name):
            if name not in var_map:
                var_map[name] = Utils.random_var()
            return var_map[name]
        
        def replace_local(match):
            var = match.group(1)
            if var in keywords:
                return match.group(0)
            return f'local {get_new_name(var)}'
        
        code = re.sub(r'local\s+([a-zA-Z_][a-zA-Z0-9_]*)', replace_local, code)
        
        for old, new in var_map.items():
            code = re.sub(rf'\b{re.escape(old)}\b', new, code)
        
        return code
    
    def _add_control_flow_light(self, code: str) -> str:
        """Lightweight control flow obfuscation"""
        v = Utils.random_var()
        
        opaque = f'''local {v}=(function()return type(_G)=="table"end)()
if not {v} then return end
'''
        return opaque + code
    
    def _minify(self, code: str) -> str:
        """Minify code"""
        # Remove multi-line comments
        code = re.sub(r'--\[\[[\s\S]*?\]\]', '', code)
        # Remove single-line comments (but keep our watermark)
        code = re.sub(r'(?<!-)--(?!\[\[)[^\n]*', '', code)
        
        # Compress whitespace
        lines = []
        for line in code.split('\n'):
            line = line.strip()
            if line:
                # Compress multiple spaces
                line = re.sub(r'\s+', ' ', line)
                lines.append(line)
        
        return ' '.join(lines)
    
    def _create_loader_optimized(self, code: str, layers: int = 1) -> str:
        """Optimized multi-layer loader"""
        
        # Generate custom base64
        chars = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")
        random.shuffle(chars)
        alphabet = ''.join(chars)
        
        # Encode
        encoded = code
        for _ in range(layers):
            standard = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
            b64 = base64.b64encode(encoded.encode()).decode()
            encoded = ''.join(alphabet[standard.index(c)] if c in standard else c for c in b64)
        
        # Compact decoder
        d = Utils.random_var()
        data = Utils.random_var()
        
        decoder = f'''local {d}=(function()local a="{alphabet}"return function(s)local r,b,n="",0,0 for i=1,#s do local c=s:sub(i,i)local p=a:find(c)if p then b=b*64+(p-1)n=n+6 while n>=8 do n=n-8 r=r..string.char(math.floor(b/2^n)%256)end end end return r end end)()
'''
        
        loader = decoder
        loader += f'local {data}="{encoded}"\n'
        
        # Decode layers
        prev = data
        for i in range(layers):
            new_var = Utils.random_var()
            loader += f'local {new_var}={d}({prev})\n'
            prev = new_var
        
        # Execute
        loader += f'(loadstring or load)({prev})()\n'
        
        return loader
    
    def obfuscate(self, code: str, level: str = None, 
                  config: dict = None, hwid_list: list = None) -> tuple:
        """
        Main obfuscation method
        
        Args:
            code: Source Lua code
            level: Preset level name (optional if config provided)
            config: Custom configuration dict (optional)
            hwid_list: List of allowed HWIDs
        
        Returns:
            (obfuscated_code, stats)
        """
        
        start_time = time.time()
        original_size = len(code)
        
        # Get configuration
        if config:
            # Use custom config
            cfg = self.get_default_config()
            cfg.update(config)
        elif level and level in self.PRESETS:
            cfg = self.PRESETS[level].copy()
        else:
            cfg = self.PRESETS['standard'].copy()
            level = 'standard'
        
        if hwid_list:
            cfg['hwid_lock'] = True
        
        result = code
        layers = []
        
        try:
            # Step 1: Variable renaming (no size/performance impact)
            if cfg.get('variable_rename'):
                result = self._rename_variables(result)
                layers.append('Variable Rename')
            
            # Step 2: String encryption
            if cfg.get('string_encryption'):
                result = self._encrypt_strings_optimized(result)
                layers.append('String Encryption')
            
            # Step 3: Control flow (light version)
            if cfg.get('control_flow'):
                result = self._add_control_flow_light(result)
                layers.append('Control Flow')
            
            # Step 4: Junk code (adjustable intensity)
            if cfg.get('junk_code'):
                intensity = cfg.get('junk_intensity', 2)
                if intensity > 0:
                    result = self.junk.inject_junk(result, intensity)
                    layers.append(f'Junk Code (x{intensity})')
            
            # Step 5: Anti-tamper
            if cfg.get('anti_tamper'):
                protection = self.anti_tamper.generate_integrity_check()
                if cfg.get('anti_debug'):
                    protection += self.anti_tamper.generate_anti_debug()
                if cfg.get('hwid_lock') and hwid_list:
                    protection += self.anti_tamper.generate_hwid_check(hwid_list)
                    layers.append('HWID Lock')
                result = protection + result
                layers.append('Anti-Tamper')
            
            # Step 6: Minify (reduces size)
            if cfg.get('minify'):
                result = self._minify(result)
                layers.append('Minify')
            
            # Step 7: VM Protection (heavy - only if enabled)
            if cfg.get('virtualization'):
                result = self.vm.generate_vm_wrapper(result)
                layers.append('VM Protection')
            
            # Step 8: Encoding layers
            comp_layers = cfg.get('compression_layers', 1)
            if comp_layers > 0:
                result = self._create_loader_optimized(result, comp_layers)
                layers.append(f'Encoding ({comp_layers}x)')
            
            # Step 9: Header
            header = self._generate_header(cfg.get('watermark_hidden', True))
            result = header + '\n' + result
            
        except Exception as e:
            raise Exception(f"Obfuscation error: {str(e)}")
        
        # Stats
        end_time = time.time()
        
        stats = {
            'original_size': original_size,
            'obfuscated_size': len(result),
            'size_ratio': f"{(len(result) / original_size * 100):.1f}%",
            'size_increase': f"+{len(result) - original_size:,} bytes",
            'level': (level or 'custom').upper(),
            'watermark': self.watermark,
            'layers_applied': layers,
            'layers_count': len(layers),
            'processing_time': f"{(end_time - start_time) * 1000:.2f}ms",
            'protection_score': self._calc_score(cfg),
            'config': cfg,
        }
        
        return result, stats
    
    def _calc_score(self, config: dict) -> str:
        """Calculate protection score"""
        score = 0
        if config.get('string_encryption'): score += 15
        if config.get('variable_rename'): score += 10
        if config.get('control_flow'): score += 10
        if config.get('junk_code'): score += config.get('junk_intensity', 0) * 2
        if config.get('anti_tamper'): score += 15
        if config.get('anti_debug'): score += 5
        if config.get('virtualization'): score += 25
        if config.get('hwid_lock'): score += 10
        score += config.get('compression_layers', 0) * 3
        
        score = min(100, score)
        stars = min(5, (score + 10) // 20)
        return f"{score}/100 {'⭐' * stars}"
    
    def estimate_impact(self, config: dict) -> dict:
        """Estimate performance/size impact of config"""
        cpu_impact = 0
        size_impact = 0
        
        impacts = {
            'string_encryption': (1, 2),
            'variable_rename': (0, 0),
            'control_flow': (1, 1),
            'junk_code': (2, 3),
            'anti_tamper': (1, 1),
            'anti_debug': (1, 1),
            'virtualization': (4, 4),
            'hwid_lock': (0, 1),
        }
        
        for feature, (cpu, size) in impacts.items():
            if config.get(feature):
                cpu_impact += cpu
                size_impact += size
        
        # Junk intensity
        if config.get('junk_code'):
            intensity = config.get('junk_intensity', 0)
            cpu_impact += intensity
            size_impact += intensity * 2
        
        # Compression layers
        layers = config.get('compression_layers', 0)
        cpu_impact += layers
        size_impact += layers
        
        # Minify reduces size
        if config.get('minify'):
            size_impact -= 2
        
        cpu_impact = max(0, min(10, cpu_impact))
        size_impact = max(0, min(10, size_impact))
        
        cpu_label = ['None', 'Very Low', 'Low', 'Medium', 'High', 'Very High'][min(5, cpu_impact // 2)]
        size_label = ['Minimal', 'Low', 'Medium', 'High', 'Very High'][min(4, size_impact // 2)]
        
        return {
            'cpu_score': cpu_impact,
            'cpu_label': cpu_label,
            'size_score': size_impact,
            'size_label': size_label,
            'recommended_for': self._get_recommendation(cpu_impact),
        }
    
    def _get_recommendation(self, cpu_impact: int) -> str:
        """Get executor recommendation based on CPU impact"""
        if cpu_impact <= 2:
            return "All executors (Delta, Fluxus, Mobile)"
        elif cpu_impact <= 4:
            return "Most executors (Fluxus, Krnl)"
        elif cpu_impact <= 6:
            return "Strong executors (Synapse, Script-Ware)"
        else:
            return "PC executors only (Synapse X)"