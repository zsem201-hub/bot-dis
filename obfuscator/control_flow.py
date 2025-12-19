import random
import re
from .utils import Utils

class ControlFlowObfuscator:
    """
    Control Flow Obfuscation
    - Control Flow Flattening
    - Opaque Predicates
    - Dead Code Insertion
    - State Machine Transformation
    """
    
    def __init__(self):
        self.state_counter = 0
    
    def generate_opaque_predicate(self, always_true: bool = True) -> str:
        """
        Generate opaque predicate - kondisi yang selalu true/false
        tapi susah dianalisis secara statis
        """
        var1 = Utils.random_name()
        var2 = Utils.random_name()
        
        predicates_true = [
            f'(function() local {var1} = math.floor(os.clock() * 1000) return {var1} >= 0 end)()',
            f'(function() local {var1} = tostring({{}}) return #{var1} > 0 end)()',
            f'(function() local {var1} = type(_G) return {var1} == "table" end)()',
            f'(function() local {var1}, {var2} = 1, 2 return {var1} < {var2} end)()',
            f'(function() return (1 + 1) == 2 end)()',
            f'(function() local {var1} = {{1}} return {var1}[1] ~= nil end)()',
            f'(function() local {var1} = "a" return {var1}:len() > 0 end)()',
            f'(function() local {var1} = math.random(1, 1000000) return {var1} > 0 end)()',
            f'(function() return string.char(65) == "A" end)()',
            f'(function() local {var1} = coroutine.create(function() end) return {var1} ~= nil end)()',
        ]
        
        predicates_false = [
            f'(function() local {var1} = type(nil) return {var1} == "number" end)()',
            f'(function() return (1 + 1) == 3 end)()',
            f'(function() local {var1} = {{}} return {var1}[1] ~= nil end)()',
            f'(function() local {var1} = "" return #{var1} > 100 end)()',
            f'(function() return tostring(1) == "2" end)()',
        ]
        
        if always_true:
            return random.choice(predicates_true)
        else:
            return random.choice(predicates_false)
    
    def generate_state_machine(self, num_states: int = 5) -> tuple:
        """Generate state machine untuk control flow flattening"""
        
        state_var = Utils.random_name()
        switch_var = Utils.random_name()
        
        # Generate random state values
        states = random.sample(range(100, 999), num_states)
        state_order = list(range(num_states))
        random.shuffle(state_order)
        
        return state_var, switch_var, states, state_order
    
    def flatten_control_flow(self, code: str) -> str:
        """
        Transform code menggunakan control flow flattening
        Mengubah struktur kode menjadi state machine
        """
        
        state_var, switch_var, states, _ = self.generate_state_machine(8)
        
        # Split code menjadi blocks
        lines = code.strip().split('\n')
        
        # Generate dispatcher
        dispatcher = f'''
local {state_var} = {states[0]}
local {switch_var} = true

while {switch_var} do
    if {state_var} == {states[0]} then
        -- Block 0: Initialization
        {self.generate_opaque_predicate(True)} and (function()
            -- Original code execution
        end)()
        {state_var} = {states[1]}
    elseif {state_var} == {states[1]} then
        -- Block 1: Main execution
'''
        
        # Add code dalam blocks
        for i, line in enumerate(lines[:5]):  # Limit untuk demo
            dispatcher += f'        {line}\n'
        
        dispatcher += f'''
        {state_var} = {states[2]}
    elseif {state_var} == {states[2]} then
        -- Block 2: Continuation
'''
        
        for i, line in enumerate(lines[5:10]):
            dispatcher += f'        {line}\n'
        
        dispatcher += f'''
        {state_var} = {states[3]}
    elseif {state_var} == {states[3]} then
        -- Block 3: Exit
        {switch_var} = false
    else
        -- Dead state
        if {self.generate_opaque_predicate(False)} then
            error("Tampering detected")
        end
        {switch_var} = false
    end
end
'''
        
        return dispatcher
    
    def add_opaque_branches(self, code: str) -> str:
        """Add opaque predicate branches ke code"""
        
        lines = code.split('\n')
        result = []
        
        for i, line in enumerate(lines):
            result.append(line)
            
            # Random chance untuk insert opaque branch
            if random.random() < 0.15 and line.strip() and not line.strip().startswith('--'):
                dead_var = Utils.random_name()
                
                # Insert opaque predicate dengan dead code
                branch = f'''
if {self.generate_opaque_predicate(False)} then
    local {dead_var} = (function()
        return string.reverse(tostring(math.random()))
    end)()
    error({dead_var})
end'''
                result.append(branch)
        
        return '\n'.join(result)
    
    def generate_fake_loops(self) -> str:
        """Generate fake loops yang tidak pernah dieksekusi"""
        var = Utils.random_name()
        counter = Utils.random_name()
        
        fake_loops = [
            f'''
if {self.generate_opaque_predicate(False)} then
    for {counter} = 1, math.huge do
        local {var} = {counter} * math.random()
        if {var} < 0 then break end
    end
end''',
            f'''
while {self.generate_opaque_predicate(False)} do
    local {var} = os.clock()
    if {var} > -1 then break end
end''',
            f'''
repeat
    local {var} = collectgarbage("count")
until {self.generate_opaque_predicate(True)}''',
        ]
        
        return random.choice(fake_loops)
