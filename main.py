import os
import threading
from flask import Flask
from bot import run_bot

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>LuaShield Pro v2.1</title>
    <style>
        body { 
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
            color: #fff; 
            font-family: 'Segoe UI', sans-serif; 
            text-align: center; 
            padding: 50px;
            min-height: 100vh;
            margin: 0;
        }
        h1 { color: #00d4ff; font-size: 3em; margin-bottom: 10px; }
        .status { color: #00ff88; font-size: 1.5em; }
        .features { 
            display: flex; 
            flex-wrap: wrap; 
            justify-content: center; 
            gap: 20px; 
            margin-top: 40px; 
        }
        .feature { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 10px; 
            width: 200px; 
        }
        .feature h3 { color: #00d4ff; margin: 0 0 10px 0; }
        .feature p { margin: 0; opacity: 0.8; }
    </style>
</head>
<body>
    <h1>🔒 LuaShield Pro v2.1</h1>
    <p class="status">✅ Bot is running!</p>
    <p>Professional Lua Obfuscator for Roblox</p>
    
    <div class="features">
        <div class="feature">
            <h3>🎛️ Custom Mode</h3>
            <p>Choose individual features</p>
        </div>
        <div class="feature">
            <h3>📱 Executor Optimized</h3>
            <p>Works with Delta, Fluxus, etc.</p>
        </div>
        <div class="feature">
            <h3>⚡ 7 Presets</h3>
            <p>From Mobile to Ultra</p>
        </div>
        <div class="feature">
            <h3>🔐 Full Protection</h3>
            <p>VM, Encryption, Anti-tamper</p>
        </div>
    </div>
</body>
</html>
'''

def run_server():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    server = threading.Thread(target=run_server)
    server.daemon = True
    server.start()
    run_bot()