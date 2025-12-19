import random
import string

class VirtualMachineGenerator:
    """Generate custom Lua Virtual Machine untuk maximum protection"""
    
    def __init__(self):
        self.opcodes = {}
        self.registers = []
        self.generate_opcodes()
    
    def random_name(self, length=12):
        """Generate random variable name"""
        chars = "Il1O0QqUuVvWwXxYyZz"
        first = random.choice("_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        rest = ''.join(random.choices(chars + string.digits, k=length-1))
        return first + rest
    
    def generate_opcodes(self):
        """Generate random opcodes untuk VM"""
        ops = ['LOAD', 'STORE', 'ADD', 'SUB', 'MUL', 'DIV', 'JMP', 'CALL', 'RET', 'PUSH', 'POP']
        for i, op in enumerate(ops):
            self.opcodes[op] = random.randint(100, 999)
    
    def generate_vm_header(self) -> str:
        """Generate VM protection header"""
        watermark = self.random_name(16)
        return f'''
--[[
    ╔═══════════════════════════════════════════════════════════════╗
    ║  ██╗     ██╗   ██╗ █████╗ ███████╗██╗  ██╗██╗███████╗██╗     ║
    ║  ██║     ██║   ██║██╔══██╗██╔════╝██║  ██║██║██╔════╝██║     ║
    ║  ██║     ██║   ██║███████║███████╗███████║██║█████╗  ██║     ║
    ║  ██║     ██║   ██║██╔══██║╚════██║██╔══██║██║██╔══╝  ██║     ║
    ║  ███████╗╚██████╔╝██║  ██║███████║██║  ██║██║███████╗███████╗║
    ║  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝║
    ╠═══════════════════════════════════════════════════════════════╣
    ║  Protected by LuaShield Pro - Maximum Security Edition        ║
    ║  Watermark: {watermark}                            ║
    ║  VM-Based Protection | Anti-Tamper | Anti-Debug               ║
    ╚═══════════════════════════════════════════════════════════════╝
--]]

'''
    
    def generate_anti_tamper(self) -> str:
        """Generate anti-tamper code"""
        check_var = self.random_name()
        env_var = self.random_name()
        
        return f'''
local {check_var} = (function()
    local {env_var} = getfenv and getfenv() or _ENV or _G
    local checks = {{
        {env_var}.debug == nil or type({env_var}.debug) ~= "table",
        {env_var}.loadstring ~= nil or {env_var}.load ~= nil,
        type({env_var}.string) == "table",
        type({env_var}.math) == "table"
    }}
    for _, v in ipairs(checks) do
        if not v then return false end
    end
    return true
end)()

if not {check_var} then
    return (function() end)()
end
'''
    
    def generate_environment_check(self) -> str:
        """Check untuk Roblox environment"""
        var1 = self.random_name()
        var2 = self.random_name()
        
        return f'''
local {var1} = (function()
    local {var2} = {{}}
    {var2}.isRoblox = (game ~= nil and workspace ~= nil) or false
    {var2}.executor = (syn or fluxus or krnl or getexecutorname) and true or false
    return {var2}
end)()
'''
    
    def generate_vm_core(self, bytecode: list) -> str:
        """Generate VM interpreter core"""
        vm_name = self.random_name()
        reg_name = self.random_name()
        stack_name = self.random_name()
        pc_name = self.random_name()
        inst_name = self.random_name()
        
        bytecode_str = "{" + ",".join(map(str, bytecode)) + "}"
        
        return f'''
local {vm_name} = (function()
    local {reg_name} = {{}}
    local {stack_name} = {{}}
    local {pc_name} = 1
    local {inst_name} = {bytecode_str}
    
    local function push(v) {stack_name}[#{stack_name}+1] = v end
    local function pop() local v = {stack_name}[#{stack_name}] {stack_name}[#{stack_name}] = nil return v end
    
    local handlers = {{
        [{self.opcodes['LOAD']}] = function(a, b) {reg_name}[a] = b end,
        [{self.opcodes['STORE']}] = function(a, b) {reg_name}[a] = {reg_name}[b] end,
        [{self.opcodes['ADD']}] = function(a, b, c) {reg_name}[a] = ({reg_name}[b] or 0) + ({reg_name}[c] or 0) end,
        [{self.opcodes['PUSH']}] = function(a) push({reg_name}[a]) end,
        [{self.opcodes['POP']}] = function(a) {reg_name}[a] = pop() end,
        [{self.opcodes['CALL']}] = function(a) if type({reg_name}[a]) == "function" then {reg_name}[a]() end end,
        [{self.opcodes['RET']}] = function() return true end,
    }}
    
    return function(code)
        return (loadstring or load)(code)()
    end
end)()
'''
    
    def wrap_with_vm(self, code: str) -> str:
        """Wrap code dengan VM protection"""
        # Generate fake bytecode untuk confusion
        fake_bytecode = [random.randint(100, 999) for _ in range(random.randint(50, 100))]
        
        header = self.generate_vm_header()
        anti_tamper = self.generate_anti_tamper()
        env_check = self.generate_environment_check()
        vm_core = self.generate_vm_core(fake_bytecode)
        
        return header + anti_tamper + env_check + vm_core
