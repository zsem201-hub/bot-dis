import random
from .utils import Utils

class JunkCodeGenerator:
    """
    Junk Code Generator
    - Dead code yang tidak pernah dieksekusi
    - Fake functions dan variables
    - Confusing logic
    - Garbage instructions
    """
    
    def __init__(self):
        pass
    
    def generate_junk_variable(self) -> str:
        """Generate junk variable declaration"""
        var = Utils.random_name()
        
        templates = [
            f'local {var} = (function() return nil end)()',
            f'local {var} = {{}}; {var}[1] = {var}',
            f'local {var} = tostring(math.random()):reverse()',
            f'local {var} = string.rep("", 0)',
            f'local {var} = #{{{random.randint(1,100)},{random.randint(1,100)}}}',
            f'local {var} = type(nil) .. type(true)',
            f'local {var} = (1 > 2) and "a" or "b"',
            f'local {var} = select(2, pcall(function() end))',
            f'local {var} = rawget(_G, "{Utils.random_name()}")',
            f'local {var} = coroutine.wrap(function() return nil end)()',
        ]
        
        return random.choice(templates)
    
    def generate_junk_function(self) -> str:
        """Generate junk function yang tidak pernah dipanggil"""
        func = Utils.random_name()
        param1 = Utils.random_name()
        param2 = Utils.random_name()
        local_var = Utils.random_name()
        
        templates = [
            f'''local function {func}({param1}, {param2})
    local {local_var} = {param1} or {param2}
    if type({local_var}) == "nil" then
        return (function() return nil end)()
    end
    return {local_var}
end''',
            f'''local {func} = function({param1})
    local {local_var} = {{}}
    for i = 1, #{param1} or 0 do
        {local_var}[i] = {param1}:sub(i, i)
    end
    return table.concat({local_var})
end''',
            f'''local {func}
{func} = function({param1}, {param2})
    if not {param1} then return {param2} end
    if not {param2} then return {param1} end
    return {func}({param2}, nil)
end''',
            f'''local {func} = setmetatable({{}}, {{
    __call = function(self, {param1})
        return rawget(self, {param1})
    end,
    __index = function(self, key)
        return nil
    end
}})''',
        ]
        
        return random.choice(templates)
    
    def generate_junk_loop(self) -> str:
        """Generate junk loop yang tidak berpengaruh"""
        var = Utils.random_name()
        counter = Utils.random_name()
        
        templates = [
            f'''for {counter} = 1, 0 do
    local {var} = {counter}
end''',
            f'''while false do
    local {var} = os.clock()
end''',
            f'''repeat
    local {var} = nil
until true''',
            f'''for {counter} = 0, -1 do
    break
end''',
            f'''if false then
    for {counter} = 1, math.huge do
        local {var} = {counter}
    end
end''',
        ]
        
        return random.choice(templates)
    
    def generate_junk_table(self) -> str:
        """Generate junk table dengan random data"""
        var = Utils.random_name()
        
        # Random table content
        entries = []
        for _ in range(random.randint(3, 8)):
            key = Utils.random_name()
            value_type = random.choice(['number', 'string', 'bool', 'table'])
            
            if value_type == 'number':
                value = str(random.randint(-1000, 1000))
            elif value_type == 'string':
                value = f'"{Utils.random_name()}"'
            elif value_type == 'bool':
                value = random.choice(['true', 'false'])
            else:
                value = '{}'
            
            entries.append(f'["{key}"] = {value}')
        
        return f'local {var} = {{{", ".join(entries)}}}'
    
    def generate_junk_math(self) -> str:
        """Generate junk mathematical operations"""
        var1 = Utils.random_name()
        var2 = Utils.random_name()
        var3 = Utils.random_name()
        
        a = random.randint(1, 1000)
        b = random.randint(1, 1000)
        
        return f'''local {var1} = {a}
local {var2} = {b}
local {var3} = ({var1} * {var2} + {var1}) / ({var2} + 1) - {var1} + {var2}
{var3} = math.floor({var3} * 0 + 0.5)'''
    
    def generate_junk_string_ops(self) -> str:
        """Generate junk string operations"""
        var = Utils.random_name()
        str_var = Utils.random_name()
        
        random_str = Utils.random_name(20)
        
        return f'''local {str_var} = "{random_str}"
local {var} = {str_var}:reverse():upper():lower():reverse()
{var} = {var}:sub(1, 0)'''
    
    def generate_junk_block(self, intensity: int = 5) -> str:
        """Generate block of junk code"""
        generators = [
            self.generate_junk_variable,
            self.generate_junk_function,
            self.generate_junk_loop,
            self.generate_junk_table,
            self.generate_junk_math,
            self.generate_junk_string_ops,
        ]
        
        blocks = []
        for _ in range(intensity):
            gen = random.choice(generators)
            blocks.append(gen())
        
        return '\n\n'.join(blocks)
    
    def inject_junk_code(self, code: str, intensity: int = 3) -> str:
        """Inject junk code ke dalam code"""
        lines = code.split('\n')
        result = []
        
        # Add junk at beginning
        result.append(f'-- Initialization\n{self.generate_junk_block(2)}')
        
        for i, line in enumerate(lines):
            result.append(line)
            
            # Random chance untuk inject junk
            if random.random() < (intensity * 0.05):
                if line.strip() and not line.strip().startswith('--'):
                    junk_type = random.choice([
                        self.generate_junk_variable,
                        self.generate_junk_math,
                        self.generate_junk_loop,
                    ])
                    result.append(junk_type())
        
        # Add junk at end
        result.append(f'\n-- Cleanup\n{self.generate_junk_block(2)}')
        
        return '\n'.join(result)
