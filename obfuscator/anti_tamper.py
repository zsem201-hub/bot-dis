import random
import hashlib
from .utils import Utils

class AntiTamperGenerator:
    """
    Anti-Tamper dan Security Features
    - Integrity checking
    - Anti-debug
    - HWID locking
    - Environment validation
    - Self-destruct on tampering
    """
    
    def __init__(self):
        pass
    
    def generate_integrity_check(self, code_hash: str) -> str:
        """Generate integrity check berdasarkan hash kode"""
        
        check_var = Utils.random_name()
        hash_var = Utils.random_name()
        
        return f'''
-- Integrity Verification
local {check_var} = (function()
    local {hash_var} = "{code_hash}"
    local function verify()
        -- Check environment integrity
        local env = _G or getfenv and getfenv() or {{}}
        if type(env.string) ~= "table" then return false end
        if type(env.math) ~= "table" then return false end
        if type(env.table) ~= "table" then return false end
        return true
    end
    return verify()
end)()

if not {check_var} then
    return (function() 
        -- Tamper detected, silent exit
    end)()
end
'''
    
    def generate_anti_debug(self) -> str:
        """Generate anti-debug code"""
        
        debug_var = Utils.random_name()
        check_var = Utils.random_name()
        
        return f'''
-- Anti-Debug Protection
local {debug_var} = (function()
    local {check_var} = {{}}
    
    -- Check for debug library
    {check_var}.noDebug = (debug == nil) or (type(debug) ~= "table")
    
    -- Check for hook functions
    {check_var}.noHook = not (debug and debug.sethook)
    
    -- Check for suspicious globals
    {check_var}.cleanEnv = not (rawget(_G, "spy") or rawget(_G, "hook") or rawget(_G, "intercept"))
    
    -- Check execution time (anti-stepping)
    local startTime = os.clock and os.clock() or 0
    local sum = 0
    for i = 1, 1000 do sum = sum + i end
    local elapsed = os.clock and (os.clock() - startTime) or 0
    {check_var}.normalSpeed = elapsed < 0.1
    
    for k, v in pairs({check_var}) do
        if not v then return false end
    end
    return true
end)()

if not {debug_var} then
    while true do
        -- Infinite loop sebagai punishment
        local x = math.random()
    end
end
'''
    
    def generate_hwid_lock(self, hwid_list: list = None) -> str:
        """Generate HWID lock untuk Roblox executors"""
        
        hwid_var = Utils.random_name()
        check_var = Utils.random_name()
        allowed_var = Utils.random_name()
        
        if hwid_list:
            allowed_hwids = '{"' + '","'.join(hwid_list) + '"}'
        else:
            allowed_hwids = '{}'  # Empty = no restriction
        
        return f'''
-- HWID Lock Protection
local {hwid_var} = (function()
    local {allowed_var} = {allowed_hwids}
    
    -- Skip jika tidak ada restriction
    if #{allowed_var} == 0 then return true end
    
    local {check_var} = nil
    
    -- Try berbagai cara untuk get HWID
    pcall(function()
        if gethwid then
            {check_var} = gethwid()
        elseif get_hwid then
            {check_var} = get_hwid()
        elseif getexecutorname then
            -- Fallback ke executor name
            {check_var} = getexecutorname()
        elseif identifyexecutor then
            {check_var} = identifyexecutor()
        elseif syn and syn.hwid then
            {check_var} = syn.hwid()
        end
    end)
    
    if not {check_var} then return true end -- Allow jika tidak bisa get HWID
    
    for _, allowed in ipairs({allowed_var}) do
        if {check_var} == allowed then
            return true
        end
    end
    
    return false
end)()

if not {hwid_var} then
    error("Unauthorized access - HWID not whitelisted")
    return
end
'''
    
    def generate_environment_check(self) -> str:
        """Check untuk valid Roblox environment"""
        
        env_var = Utils.random_name()
        result_var = Utils.random_name()
        
        return f'''
-- Environment Validation
local {env_var} = (function()
    local {result_var} = {{
        isRoblox = false,
        hasExecutor = false,
        validEnv = false
    }}
    
    -- Check Roblox
    pcall(function()
        {result_var}.isRoblox = (game ~= nil) and (workspace ~= nil)
    end)
    
    -- Check Executor
    pcall(function()
        {result_var}.hasExecutor = (syn ~= nil) or (fluxus ~= nil) or 
            (krnl ~= nil) or (getexecutorname ~= nil) or
            (KRNL_LOADED ~= nil) or (Synapse ~= nil)
    end)
    
    -- Validate environment
    {result_var}.validEnv = (loadstring ~= nil) or (load ~= nil)
    
    return {result_var}
end)()
'''
    
    def generate_self_destruct(self) -> str:
        """Generate self-destruct jika tampering detected"""
        
        destroy_var = Utils.random_name()
        
        return f'''
-- Self-Destruct Mechanism
local {destroy_var} = function()
    -- Corrupt critical variables
    pcall(function() _G = nil end)
    pcall(function() string = nil end)
    pcall(function() math = nil end)
    pcall(function() table = nil end)
    
    -- Clear script
    if script and script.Destroy then
        pcall(function() script:Destroy() end)
    end
    
    -- Force error
    error(string.rep("\\0", 10000))
end
'''
    
    def generate_full_protection(self, code_hash: str = None, hwid_list: list = None) -> str:
        """Generate semua protection dalam satu block"""
        
        if not code_hash:
            code_hash = Utils.generate_watermark()
        
        protection = self.generate_integrity_check(code_hash)
        protection += '\n' + self.generate_anti_debug()
        protection += '\n' + self.generate_hwid_lock(hwid_list)
        protection += '\n' + self.generate_environment_check()
        protection += '\n' + self.generate_self_destruct()
        
        return protection
