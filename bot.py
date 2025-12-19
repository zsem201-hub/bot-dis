import discord
from discord.ext import commands
from discord import app_commands
import io
import re
import os
import asyncio
from datetime import datetime

from obfuscator import LuaShieldPro

# ==================== CONFIG ====================
BOT_TOKEN = os.environ.get('DISCORD_TOKEN', 'YOUR_TOKEN_HERE')
PREFIX = '!'

# ==================== BOT SETUP ====================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)
obfuscator = LuaShieldPro()

# ==================== COLORS ====================
class Colors:
    PRIMARY = 0x00D4FF
    SUCCESS = 0x00FF88
    ERROR = 0xFF4444
    WARNING = 0xFFAA00
    INFO = 0x7289DA

def create_embed(title: str, desc: str = "", color: int = Colors.PRIMARY) -> discord.Embed:
    embed = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.utcnow())
    embed.set_footer(text="LuaShield Pro", icon_url=bot.user.avatar.url if bot.user.avatar else None)
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
║  Bot: {str(bot.user):<52} ║
║  Servers: {len(bot.guilds):<48} ║
║  Status: Online ✅                                           ║
╚══════════════════════════════════════════════════════════════╝
''')
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="!help | Protecting Scripts"
        )
    )
    
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Sync error: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

# ==================== COMMANDS ====================

@bot.command(name='help', aliases=['h', 'commands', 'menu'])
async def help_cmd(ctx):
    embed = create_embed("🔒 LuaShield Pro", "Professional Lua Obfuscator for Roblox")
    
    embed.add_field(
        name="📋 Commands",
        value="""
`!obf [level]` - Obfuscate Lua code
`!levels` - Show protection levels
`!features` - Show all features
`!example` - Usage example
`!ping` - Bot latency
        """,
        inline=False
    )
    
    embed.add_field(
        name="🎚️ Protection Levels",
        value="""
• `light` - Basic, fast
• `medium` - Balanced
• `standard` - Recommended ⭐
• `maximum` - VM + Full protection
• `ultra` - Ultimate security
        """,
        inline=False
    )
    
    embed.add_field(
        name="📤 How to Use",
        value="Upload `.lua` file with `!obf [level]`\nOr use code block in message",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='features')
async def features_cmd(ctx):
    embed = create_embed("🛡️ Protection Features", "")
    
    features = {
        "🖥️ Virtualization": "Code runs in custom VM, not native Lua",
        "🔀 Control Flow Flattening": "Loop/if structures destroyed",
        "🎭 Opaque Predicates": "Fake if-else that always true/false",
        "🔐 String Encryption": "All strings encrypted with XOR",
        "📦 Bytecode Encryption": "Code encrypted, decrypted at runtime",
        "🛡️ Anti-Tamper": "Self-check, crash if modified",
        "🔑 HWID Lock": "Only runs on specific devices",
        "📚 Multi-Layer": "Multiple obfuscation layers",
        "🗑️ Junk Code": "Garbage code to confuse",
        "🔄 Dynamic Keys": "Encryption key changes every build",
    }
    
    for name, desc in features.items():
        embed.add_field(name=name, value=desc, inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='levels', aliases=['lvl'])
async def levels_cmd(ctx):
    embed = create_embed("🎚️ Protection Levels", "Choose your protection level")
    
    levels = [
        ("💨 Light", "String Encryption, Variable Rename\nScore: ⭐ (20/100)\nBest for: Quick protection"),
        ("⚖️ Medium", "Light + Control Flow, Anti-Tamper, Junk Code\nScore: ⭐⭐⭐ (55/100)\nBest for: Normal scripts"),
        ("🛡️ Standard", "Medium + Bytecode Encryption\nScore: ⭐⭐⭐⭐ (65/100)\nBest for: Most scripts"),
        ("🔐 Maximum", "Standard + VM Virtualization\nScore: ⭐⭐⭐⭐⭐ (90/100)\nBest for: Important scripts"),
        ("💎 Ultra", "All features + HWID Lock\nScore: ⭐⭐⭐⭐⭐ (100/100)\nBest for: Premium protection"),
    ]
    
    for name, desc in levels:
        embed.add_field(name=name, value=desc, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='example')
async def example_cmd(ctx):
    embed = create_embed("📖 Usage Examples", "")
    
    embed.add_field(
        name="Method 1: File Upload",
        value="1. Upload your `.lua` file\n2. Type `!obf maximum`\n3. Get protected file!",
        inline=False
    )
    
    embed.add_field(
        name="Method 2: Code Block",
        value='```\n!obf ultra\n```lua\nlocal player = game.Players.LocalPlayer\nprint("Hello!")\n```\n```',
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping_cmd(ctx):
    latency = round(bot.latency * 1000)
    status = "🟢 Excellent" if latency < 100 else "🟡 Good" if latency < 200 else "🔴 High"
    await ctx.send(embed=create_embed("🏓 Pong!", f"Latency: **{latency}ms** {status}"))

@bot.command(name='obfuscate', aliases=['obf', 'o', 'protect', 'enc'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def obfuscate_cmd(ctx, level: str = "standard"):
    """Main obfuscation command"""
    
    valid_levels = ['light', 'medium', 'standard', 'maximum', 'ultra']
    if level.lower() not in valid_levels:
        embed = create_embed("⚠️ Invalid Level", 
            f"Valid: `{', '.join(valid_levels)}`\nUsing `standard`", Colors.WARNING)
        await ctx.send(embed=embed)
        level = "standard"
    
    # Get code
    code = None
    filename = "script.lua"
    
    if ctx.message.attachments:
        att = ctx.message.attachments[0]
        if att.filename.endswith(('.lua', '.txt')):
            try:
                code = (await att.read()).decode('utf-8')
                filename = att.filename
            except:
                await ctx.send(embed=create_embed("❌ Error", "Failed to read file", Colors.ERROR))
                return
    
    if not code:
        match = re.search(r'```(?:lua)?\s*([\s\S]+?)```', ctx.message.content)
        if match:
            code = match.group(1).strip()
    
    if not code:
        embed = create_embed("📝 No Code", 
            "**Upload a `.lua` file** with the command\n**OR use code block:**\n```\n!obf maximum\n```lua\nyour code\n```\n```",
            Colors.WARNING)
        await ctx.send(embed=embed)
        return
    
    if len(code) > 200000:
        await ctx.send(embed=create_embed("❌ Too Large", "Max: 200KB", Colors.ERROR))
        return
    
    # Process
    msg = await ctx.send(embed=create_embed(
        "⏳ Processing...",
        f"**Level:** {level.upper()}\n**Size:** {len(code)} bytes\n\n🔄 Applying protection layers...",
        Colors.INFO
    ))
    
    try:
        result, stats = obfuscator.obfuscate(code, level.lower())
        
        out_name = filename.rsplit('.', 1)[0] + '_protected.lua'
        file = discord.File(io.BytesIO(result.encode('utf-8')), filename=out_name)
        
        embed = create_embed("✅ Protection Complete!", 
            f"Protected with **{level.upper()}** level", Colors.SUCCESS)
        
        embed.add_field(
            name="📊 Statistics",
            value=f"""```
Original:    {stats['original_size']:,} bytes
Protected:   {stats['obfuscated_size']:,} bytes  
Ratio:       {stats['size_ratio']}
Time:        {stats['processing_time']}
Score:       {stats['protection_score']}
```""",
            inline=False
        )
        
        embed.add_field(
            name="🛡️ Layers Applied",
            value="• " + "\n• ".join(stats['layers_applied']),
            inline=True
        )
        
        embed.add_field(
            name="🔑 Watermark",
            value=f"`{stats['watermark']}`",
            inline=True
        )
        
        await msg.edit(embed=embed)
        await ctx.send(file=file)
        
    except Exception as e:
        await msg.edit(embed=create_embed("❌ Failed", str(e), Colors.ERROR))

@obfuscate_cmd.error
async def obf_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=create_embed("⏳ Cooldown", 
            f"Wait **{error.retry_after:.1f}s**", Colors.WARNING))

# ==================== SLASH COMMANDS ====================
@bot.tree.command(name="obfuscate", description="Protect your Lua script")
@app_commands.describe(level="Protection level", code="Lua code (optional if uploading file)")
@app_commands.choices(level=[
    app_commands.Choice(name="💨 Light", value="light"),
    app_commands.Choice(name="⚖️ Medium", value="medium"),
    app_commands.Choice(name="🛡️ Standard", value="standard"),
    app_commands.Choice(name="🔐 Maximum", value="maximum"),
    app_commands.Choice(name="💎 Ultra", value="ultra"),
])
async def slash_obfuscate(interaction: discord.Interaction, level: str = "standard", code: str = None):
    await interaction.response.defer()
    
    if not code:
        await interaction.followup.send(embed=create_embed("📝 No Code", "Provide code parameter", Colors.WARNING))
        return
    
    try:
        result, stats = obfuscator.obfuscate(code, level)
        file = discord.File(io.BytesIO(result.encode('utf-8')), filename='protected.lua')
        embed = create_embed("✅ Done!", f"Level: **{level.upper()}** | Score: {stats['protection_score']}", Colors.SUCCESS)
        await interaction.followup.send(embed=embed, file=file)
    except Exception as e:
        await interaction.followup.send(embed=create_embed("❌ Error", str(e), Colors.ERROR))

# ==================== RUN ====================
def run_bot():
    if BOT_TOKEN == 'YOUR_TOKEN_HERE':
        print("❌ Set DISCORD_TOKEN in Replit Secrets!")
        return
    bot.run(BOT_TOKEN)

if __name__ == '__main__':
    run_bot()
