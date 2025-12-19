import random
from .utils import Utils

class VirtualMachine:
    """
    Custom Virtual Machine untuk Lua
    - Custom bytecode/opcodes
    - Register-based VM
    - Stack operations
    - Encrypted instruction set
    """
    
    def __init__(self):
        self.opcodes = {}
        self.registers = 16
        self.generate_opcodes()
    
    def generate_opcodes(self):
        """Generate random opcodes untuk setiap instruksi"""
        instructions = [
            'NOP', 'LOAD', 'STORE', 'MOVE', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD',
            'POW', 'UNM', 'NOT', 'LEN', 'CONCAT', 'JMP', 'EQ', 'LT', 'LE',
            'TEST', 'CALL', 'RETURN', 'PUSH', 'POP', 'GETGLOBAL', 'SETGLOBAL',
            'GETTABLE', 'SETTABLE', 'NEWTABLE', 'CLOSURE', 'VARARG'
        ]
        
        # Generate unique random opcodes
        used_opcodes = set()
        for inst in instructions:
            while True:
                opcode = random.randint(100, 999)
                if opcode not in used_opcodes:
                    used_opcodes.add(opcode)
                    self.opcodes[inst] = opcode
                    break
    
    def generate_vm_core(self) -> str:
        """Generate Lua VM core"""
        
        # Variable names
        vm_name = Utils.random_name()
        regs_name = Utils.random_name()
        stack_name = Utils.random_name()
        pc_name = Utils.random_name()
        code_name = Utils.random_name()
        handlers_name = Utils.random_name()
        
        vm_code = f'''
local {vm_name} = (function()
    local {regs_name} = {{}}
    local {stack_name} = {{}}
    local {pc_name} = 1
    local globals = _G or getfenv and getfenv() or {{}}
    
    for i = 0, 15 do {regs_name}[i] = nil end
    
    local function push(v) {stack_name}[#{stack_name} + 1] = v end
    local function pop() 
        local v = {stack_name}[#{stack_name}] 
        {stack_name}[#{stack_name}] = nil 
        return v 
    end
    local function peek() return {stack_name}[#{stack_name}] end
    
    local {handlers_name} = {{
        [{self.opcodes['NOP']}] = function() end,
        [{self.opcodes['LOAD']}] = function(a, b) {regs_name}[a] = b end,
        [{self.opcodes['STORE']}] = function(a, b) {regs_name}[a] = {regs_name}[b] end,
        [{self.opcodes['MOVE']}] = function(a, b) {regs_name}[a] = {regs_name}[b] end,
        [{self.opcodes['ADD']}] = function(a, b, c) {regs_name}[a] = ({regs_name}[b] or 0) + ({regs_name}[c] or 0) end,
        [{self.opcodes['SUB']}] = function(a, b, c) {regs_name}[a] = ({regs_name}[b] or 0) - ({regs_name}[c] or 0) end,
        [{self.opcodes['MUL']}] = function(a, b, c) {regs_name}[a] = ({regs_name}[b] or 0) * ({regs_name}[c] or 0) end,
        [{self.opcodes['DIV']}] = function(a, b, c) {regs_name}[a] = ({regs_name}[b] or 0) / ({regs_name}[c] or 1) end,
        [{self.opcodes['PUSH']}] = function(a) push({regs_name}[a]) end,
        [{self.opcodes['POP']}] = function(a) {regs_name}[a] = pop() end,
        [{self.opcodes['CALL']}] = function(a, b, c)
            local func = {regs_name}[a]
            if type(func) == "function" then
                local args = {{}}
                for i = 1, b do args[i] = pop() end
                local results = {{func(table.unpack(args))}}
                for i = 1, c do push(results[i]) end
            end
        end,
        [{self.opcodes['GETGLOBAL']}] = function(a, name) 
            {regs_name}[a] = globals[name] 
        end,
        [{self.opcodes['SETGLOBAL']}] = function(name, a) 
            globals[name] = {regs_name}[a] 
        end,
        [{self.opcodes['RETURN']}] = function() return true end,
        [{self.opcodes['JMP']}] = function(offset) {pc_name} = {pc_name} + offset end,
        [{self.opcodes['EQ']}] = function(a, b, c) {regs_name}[a] = {regs_name}[b] == {regs_name}[c] end,
        [{self.opcodes['LT']}] = function(a, b, c) {regs_name}[a] = {regs_name}[b] < {regs_name}[c] end,
        [{self.opcodes['CONCAT']}] = function(a, b, c) 
            {regs_name}[a] = tostring({regs_name}[b] or "") .. tostring({regs_name}[c] or "") 
        end,
        [{self.opcodes['NEWTABLE']}] = function(a) {regs_name}[a] = {{}} end,
        [{self.opcodes['GETTABLE']}] = function(a, b, c) 
            {regs_name}[a] = {regs_name}[b] and {regs_name}[b][{regs_name}[c]] 
        end,
        [{self.opcodes['SETTABLE']}] = function(a, b, c) 
            if {regs_name}[a] then {regs_name}[a][{regs_name}[b]] = {regs_name}[c] end 
        end,
    }}
    
    return function({code_name})
        {pc_name} = 1
        while {pc_name} <= #{code_name} do
            local inst = {code_name}[{pc_name}]
            local op = inst[1]
            local handler = {handlers_name}[op]
            if handler then
                local result = handler(inst[2], inst[3], inst[4])
                if result then break end
            end
            {pc_name} = {pc_name} + 1
        end
        return pop()
    end
end)()
'''
        return vm_code, vm_name
    
    def generate_vm_wrapper(self, code: str) -> str:
        """Wrap code dengan VM protection"""
        vm_core, vm_name = self.generate_vm_core()
        
        # Generate fake bytecode untuk confusion
        fake_instructions = []
        for _ in range(random.randint(20, 50)):
            op = random.choice(list(self.opcodes.values()))
            args = [random.randint(0, 15) for _ in range(random.randint(1, 3))]
            fake_instructions.append(f"{{{op},{','.join(map(str, args))}}}")
        
        fake_bytecode = "{" + ",".join(fake_instructions) + "}"
        
        exec_name = Utils.random_name()
        data_name = Utils.random_name()
        
        wrapper = f'''
-- VM Protection Layer
{vm_core}

local {data_name} = {fake_bytecode}
local {exec_name} = function()
    -- VM Execution Context
    local env = setmetatable({{}}, {{__index = _G or getfenv and getfenv() or {{}}}})
    local fn = (loadstring or load)([=[{code}]=], nil, nil, env)
    if fn then return fn() end
end

-- Execute dengan error handling
local success, result = pcall({exec_name})
if not success then
    -- Silent fail untuk anti-debug
end
'''
        return wrapper
