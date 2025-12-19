import os
import threading
from flask import Flask
from bot import run_bot

# Keep alive server untuk Replit
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
        <head><title>LuaShield Pro</title></head>
        <body style="background:#1a1a2e;color:#fff;font-family:monospace;text-align:center;padding:50px">
            <h1>🔒 LuaShield Pro</h1>
            <p>Professional Lua Obfuscator Bot</p>
            <p style="color:#00ff88">✅ Bot is running!</p>
        </body>
    </html>
    '''

def run_server():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    # Start web server in background
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Run Discord bot
    run_bot()
