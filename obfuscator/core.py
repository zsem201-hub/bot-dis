import random
import time
import hashlib
from .encryption import LuaEncryption
from .vm_generator import VirtualMachineGenerator
from .layers import ObfuscationLayers

class LuaShieldObfuscator:
    """
    LuaShield Pro - Professional Lua Obfuscator
    Mirip dengan Luraph/Luarmor
    """
    
    LEVELS = {
        'light': {
            'string_encryption': False,
            'variable_rename': True,
            'control_flow': False,
            'number_encoding': False,
            'junk_code': False,
            'compression_layers': 1,
            'vm_protection': False,
            'anti_tamper': False
        },
        'medium': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': True,
            'number_encoding': False,
            'junk_code': True,
            'compression_layers': 2,
            'vm_protection': False,
            'anti_tamper': True
        },
        'standard': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': True,
            'number_encoding': True,
            'junk_code': True,
            'compression_layers': 2,
            'vm_protection': False,
            'anti_tamper': True
        },
        'maximum': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': True,
            'number_encoding': True,
            'junk_code': True,
            'compression_layers': 3,
            'vm_protection': True,
            'anti_tamper': True
        },
        'ultra': {
            'string_encryption': True,
            'variable_rename': True,
            'control_flow': True,
            'number_encoding': True,
            'junk_code': True,
            'compression_layers': 4,
            'vm_protection': True,
            'anti_tamper': True
        }
    }
    
    def __init__(self):
        self.encryption = LuaEncryption()
        self.vm_gen = VirtualMachineGenerator()
        self.layers = ObfuscationLayers()
        self.stats = {}
    
    def generate_watermark(self, script_id: str = None) -> str:
        """Generate unique watermark"""
        timestamp = str(time.time())
        random_str = ''.join(random.choices('abcdef0123456789', k=8))
        data = f"{timestamp}-{random_str}-{script_id or 'default'}"
        return hashlib.md5(data.encode()).hexdigest()[:16].upper()
    
    def generate_header(self, level: str, watermark: str) -> str:
        """Generate protection header berdasarkan level"""
        
        if level in ['maximum', 'ultra']:
            return f'''--[[
╔══════════════════════════════════════════════════════════════════════╗
║  ██╗     ██╗   ██╗ █████╗ ███████╗██╗  ██╗██╗███████╗██╗     ██████╗ ║
║  ██║     ██║   ██║██╔══██╗██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗║
║  ██║     ██║   ██║███████║███████╗███████║██║█████╗  ██║     ██║  ██║║
║  ██║     ██║   ██║██╔══██║╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║║
║  ███████╗╚██████╔╝██║  ██║███████║██║  ██║██║███████╗███████╗██████╔╝║
║  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝ ║
╠══════════════════════════════════════════════════════════════════════╣
║  🔒 MAXIMUM SECURITY PROTECTION                                      ║
║  ├─ VM-Based Encryption: ENABLED                                     ║
║  ├─ Anti-Tamper: ENABLED                                             ║
║  ├─ Anti-Debug: ENABLED                                              ║
║  └─ Multi-Layer Encoding: ENABLED                                    ║
╠══════════════════════════════════════════════════════════════════════╣
║  Watermark: {watermark}                                     ║
║  Protected by LuaShield Pro | discord.gg/luashield                   ║
╚══════════════════════════════════════════════════════════════════════╝
--]]

'''
        elif level == 'standard':
            return f'''--[[
    ╔════════════════════════════════════════════════╗
    ║  LuaShield Pro - Standard Protection           ║
    ║  Watermark: {watermark}                ║
    ║  Unauthorized copying is prohibited            ║
    ╚════════════════════════════════════════════════╝
--]]

'''
        else:
            return f'-- Protected by LuaShield | {watermark}\n\n'
    
    def obfuscate(self, code: str, level: str = 'standard', script_id: str = None) -> tuple:
        """
        Main obfuscation function
        Returns: (obfuscated_code, stats_dict)
        """
        start_time = time.time()
        original_size = len(code)
        
        # Validate level
        if level not in self.LEVELS:
            level = 'standard'
        
        config = self.LEVELS[level]
        watermark = self.generate_watermark(script_id)
        
        # Reset layers untuk fresh obfuscation
        self.layers = ObfuscationLayers()
        
        result = code
        applied_layers = []
        
        try:
            # Layer 1: Variable Renaming
            if config['variable_rename']:
                result = self.layers.rename_variables(result)
                applied_layers.append('Variable Rename')
            
            # Layer 2: String Encryption
            if config['string_encryption']:
                result = self.layers.encrypt_strings(result)
                applied_layers.append('String Encryption')
            
            # Layer 3: Number Encoding
            if config['number_encoding']:
                result = self.layers.encode_numbers(result)
                applied_layers.append('Number Encoding')
            
            # Layer 4: Control Flow Obfuscation
            if config['control_flow']:
                result = self.layers.obfuscate_control_flow(result)
                applied_layers.append('Control Flow')
            
            # Layer 5: Junk Code Injection
            if config['junk_code']:
                result = self.layers.add_junk_code(result, intensity=5 if level in ['maximum', 'ultra'] else 3)
                applied_layers.append('Junk Code')
            
            # Layer 6: Compression & Encoding
            if config['compression_layers'] > 0:
                result = self.layers.compress_and_encode(result, config['compression_layers'])
                applied_layers.append(f'{config["compression_layers"]}x Encoding')
            
            # Layer 7: VM Protection
            if config['vm_protection']:
                vm_wrapper = self.vm_gen.wrap_with_vm(result)
                result = vm_wrapper + '\n' + result
                applied_layers.append('VM Protection')
            
            # Layer 8: Anti-Tamper
            if config['anti_tamper']:
                anti_tamper = self.vm_gen.generate_anti_tamper()
                result = anti_tamper + '\n' + result
                applied_layers.append('Anti-Tamper')
            
            # Add header
            header = self.generate_header(level, watermark)
            result = header + result
            
        except Exception as e:
            raise Exception(f"Obfuscation failed: {str(e)}")
        
        # Calculate stats
        end_time = time.time()
        final_size = len(result)
        
        stats = {
            'original_size': original_size,
            'obfuscated_size': final_size,
            'size_ratio': f"{(final_size / original_size * 100):.1f}%",
            'level': level.upper(),
            'watermark': watermark,
            'layers_applied': applied_layers,
            'processing_time': f"{(end_time - start_time) * 1000:.2f}ms",
            'protection_score': self._calculate_protection_score(config)
        }
        
        return result, stats
    
    def _calculate_protection_score(self, config: dict) -> str:
        """Calculate protection score"""
        score = 0
        if config['string_encryption']: score += 15
        if config['variable_rename']: score += 10
        if config['control_flow']: score += 15
        if config['number_encoding']: score += 10
        if config['junk_code']: score += 10
        if config['vm_protection']: score += 25
        if config['anti_tamper']: score += 15
        score += config['compression_layers'] * 5
        
        if score >= 90:
            return f"{score}/100 ⭐⭐⭐⭐⭐"
        elif score >= 70:
            return f"{score}/100 ⭐⭐⭐⭐"
        elif score >= 50:
            return f"{score}/100 ⭐⭐⭐"
        elif score >= 30:
            return f"{score}/100 ⭐⭐"
        else:
            return f"{score}/100 ⭐"
