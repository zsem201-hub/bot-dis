import discord
from discord.ext import commands
from discord import app_commands
import io
import re
import os
import asyncio
from datetime import datetime

# Import obfuscator
from obfuscator import LuaShieldObfuscator

# ==================== CONFIG ====================
BOT_TOKEN = os.environ.get('DISCORD_TOKEN', 'YOUR_BOT_TOKEN_HERE')
PREFIX = '!'

# ==================== BOT SETUP ====================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)
obfuscator = LuaShieldObfuscator()

# ==================== EMBEDS ====================
class EmbedBuilder:
    COLORS = {
        'primary': 0x00D4FF,
        'success': 0x00FF88,
        'error': 0xFF4444,
        'warning': 0xFFAA00,
        'info': 0x7289DA
    }
    
    @staticmethod
    def create(title: str, description: str = "", color: str = 'primary') -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            color=EmbedBuilder.COLORS.get(color, 0x00D4FF),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="LuaShield Pro", icon_url="https://i.imgur.com/xyz.png")
        return embed

# ==================== EVENTS ====================
@bot.event
async def on_ready():
    print(f'''
╔══════════════════════════════════════════════════════════════╗
║  ██╗     ██╗   ██╗ █████╗ ███████╗██╗  ██╗██╗███████╗██╗     ║
║  ██║     ██║   ██║██╔══██╗██╔════╝██║  ██║██║██╔════╝██║     ║
║  ██║     ██║   ██║███████║███████╗███████║██║█████╗  ██║     ║
║  ██║     ██║   ██║██╔══██║╚════██║██╔══██║██║██╔══╝  ██║     ║
║  ███████╗╚██████╔╝██║  ██║███████║██║  ██║██║███████╗███████╗║
║  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝║
╠══════════════════════════════════════════════════════════════╣
║  Bot: {bot.user.name:<52} ║
║  ID: {bot.user.id:<53} ║
║  Servers: {len(bot.guilds):<48} ║
╚══════════════════════════════════════════════════════════════╝
''')
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="!help | Protecting Lua Scripts"
        )
    )
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

# ==================== COMMANDS ====================

@bot.command(name='help', aliases=['h', 'commands'])
async def help_command(ctx):
    embed = EmbedBuilder.create(
        "🔒 LuaShield Pro - Help",
        "Professional Lua Obfuscator for Roblox Scripts"
    )
    
    embed.add_field(
        name="📋 Commands",
        value="""
`!obfuscate [level]` - Obfuscate Lua code
`!obf [level]` - Short alias
`!levels` - Show protection levels
`!example` - Show usage example
`!ping` - Check bot latency
`!stats` - Bot statistics
        """,
        inline=False
    )
    
    embed.add_field(
        name="🎚️ Protection Levels",
        value="""
`light` - Basic protection, fast
`medium` - Balanced protection
`standard` - Recommended ⭐
`maximum` - Maximum protection + VM
`ultra` - Ultimate protection
        """,
        inline=False
    )
    
    embed.add_field(
        name="📤 How to Use",
        value="""
**Option 1:** Upload `.lua` file with command
**Option 2:** Use code block:
