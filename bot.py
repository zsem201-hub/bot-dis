import discord
from discord.ext import commands
from discord import app_commands, ui
import io
import re
import os
import asyncio
from datetime import datetime
from typing import Optional

from obfuscator import LuaShieldPro

# Config
TOKEN = os.environ.get('DISCORD_TOKEN', 'YOUR_TOKEN')
PREFIX = '!'

# Bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)
obf = LuaShieldPro()

# Store user configs temporarily
user_configs = {}
user_code = {}

# Colors
class C:
    BLUE = 0x00D4FF
    GREEN = 0x00FF88
    RED = 0xFF4444
    YELLOW = 0xFFAA00
    PURPLE = 0x9B59B6

def embed(title, desc="", color=C.BLUE):
    e = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.utcnow())
    e.set_footer(text="LuaShield Pro v2.1")
    return e


# ==================== CUSTOM UI COMPONENTS ====================

class FeatureSelect(ui.Select):
    """Dropdown untuk memilih features"""
    
    def __init__(self):
        options = [
            discord.SelectOption(
                label="String Encryption",
                value="string_encryption",
                emoji="🔐",
                description="Encrypt all strings"
            ),
            discord.SelectOption(
                label="Variable Rename",
                value="variable_rename", 
                emoji="📝",
                description="Rename variables"
            ),
            discord.SelectOption(
                label="Control Flow",
                value="control_flow",
                emoji="🔀",
                description="Add opaque predicates"
            ),
            discord.SelectOption(
                label="Junk Code",
                value="junk_code",
                emoji="🗑️",
                description="Insert dead code (increases size)"
            ),
            discord.SelectOption(
                label="Anti-Tamper",
                value="anti_tamper",
                emoji="🛡️",
                description="Integrity checks"
            ),
            discord.SelectOption(
                label="Anti-Debug",
                value="anti_debug",
                emoji="🚫",
                description="Detect debugging"
            ),
            discord.SelectOption(
                label="VM Protection",
                value="virtualization",
                emoji="🖥️",
                description="Custom VM (heavy)"
            ),
            discord.SelectOption(
                label="HWID Lock",
                value="hwid_lock",
                emoji="🔑",
                description="Lock to devices"
            ),
            discord.SelectOption(
                label="Minify",
                value="minify",
                emoji="📦",
                description="Remove whitespace"
            ),
        ]
        
        super().__init__(
            placeholder="Select features...",
            min_values=0,
            max_values=len(options),
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        
        if user_id not in user_configs:
            user_configs[user_id] = obf.get_default_config()
        
        # Reset all features first
        for feature in obf.get_feature_list():
            user_configs[user_id][feature] = False
        
        # Enable selected features
        for value in self.values:
            user_configs[user_id][value] = True
        
        # Calculate impact
        impact = obf.estimate_impact(user_configs[user_id])
        
        # Update embed
        selected = ", ".join(self.values) if self.values else "None"
        
        e = embed("🎛️ Custom Configuration", f"**Selected:** {len(self.values)} features")
        e.add_field(
            name="✅ Enabled Features",
            value="\n".join([f"• {v.replace('_', ' ').title()}" for v in self.values]) or "None",
            inline=True
        )
        e.add_field(
            name="📊 Impact Analysis",
            value=f"**CPU:** {impact['cpu_label']}\n**Size:** {impact['size_label']}\n**Best for:** {impact['recommended_for']}",
            inline=True
        )
        
        await interaction.response.edit_message(embed=e)


class CompressionSelect(ui.Select):
    """Dropdown untuk compression layers"""
    
    def __init__(self):
        options = [
            discord.SelectOption(label="1 Layer (Fastest)", value="1", emoji="1️⃣"),
            discord.SelectOption(label="2 Layers (Balanced)", value="2", emoji="2️⃣"),
            discord.SelectOption(label="3 Layers (Strong)", value="3", emoji="3️⃣"),
            discord.SelectOption(label="4 Layers (Maximum)", value="4", emoji="4️⃣"),
        ]
        super().__init__(placeholder="Compression layers...", options=options)
    
    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id not in user_configs:
            user_configs[user_id] = obf.get_default_config()
        
        user_configs[user_id]['compression_layers'] = int(self.values[0])
        
        await interaction.response.send_message(
            f"✅ Compression set to **{self.values[0]}** layers",
            ephemeral=True
        )


class JunkIntensitySelect(ui.Select):
    """Dropdown untuk junk code intensity"""
    
    def __init__(self):
        options = [
            discord.SelectOption(label="None (0)", value="0", emoji="0️⃣"),
            discord.SelectOption(label="Minimal (1)", value="1", emoji="1️⃣"),
            discord.SelectOption(label="Low (2)", value="2", emoji="2️⃣"),
            discord.SelectOption(label="Medium (3)", value="3", emoji="3️⃣"),
            discord.SelectOption(label="High (4)", value="4", emoji="4️⃣"),
            discord.SelectOption(label="Maximum (5)", value="5", emoji="5️⃣"),
        ]
        super().__init__(placeholder="Junk code intensity...", options=options)
    
    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id not in user_configs:
            user_configs[user_id] = obf.get_default_config()
        
        user_configs[user_id]['junk_intensity'] = int(self.values[0])
        
        await interaction.response.send_message(
            f"✅ Junk intensity set to **{self.values[0]}**",
            ephemeral=True
        )


class CustomView(ui.View):
    """Main view untuk custom configuration"""
    
    def __init__(self, code: str = None):
        super().__init__(timeout=300)  # 5 minute timeout
        self.code = code
        self.add_item(FeatureSelect())
        self.add_item(CompressionSelect())
        self.add_item(JunkIntensitySelect())
    
    @ui.button(label="Apply & Obfuscate", style=discord.ButtonStyle.green, emoji="🚀", row=3)
    async def apply_button(self, interaction: discord.Interaction, button: ui.Button):
        user_id = interaction.user.id
        
        if user_id not in user_configs:
            await interaction.response.send_message("❌ Please select features first!", ephemeral=True)
            return
        
        code = user_code.get(user_id)
        if not code:
            await interaction.response.send_message("❌ No code stored! Use `!custom` with code first.", ephemeral=True)
            return
        
        await interaction.response.defer()
        
        try:
            result, stats = obf.obfuscate(code, config=user_configs[user_id])
            
            file = discord.File(io.BytesIO(result.encode('utf-8')), filename='custom_protected.lua')
            
            e = embed("✅ Custom Protection Complete!", "", C.GREEN)
            e.add_field(
                name="📊 Statistics",
                value=f"```\nOriginal:  {stats['original_size']:,} bytes\nProtected: {stats['obfuscated_size']:,} bytes\nIncrease:  {stats['size_increase']}\nTime:      {stats['processing_time']}\nScore:     {stats['protection_score']}```",
                inline=False
            )
            e.add_field(
                name="🛡️ Applied Layers",
                value="• " + "\n• ".join(stats['layers_applied']),
                inline=True
            )
            e.add_field(
                name="🔑 Watermark",
                value=f"`{stats['watermark']}`",
                inline=True
            )
            
            await interaction.followup.send(embed=e, file=file)
            
            # Cleanup
            del user_configs[user_id]
            del user_code[user_id]
            
        except Exception as ex:
            await interaction.followup.send(embed=embed("❌ Error", str(ex), C.RED))
    
    @ui.button(label="Use Preset", style=discord.ButtonStyle.blurple, emoji="📋", row=3)
    async def preset_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message(
            embed=embed("📋 Available Presets", 
                "Use `!obf <level>` with:\n\n"
                "**Performance Focused:**\n"
                "`mobile` - Minimal, for weak executors\n"
                "`delta` - Optimized for Delta executor\n"
                "`light` - Fast, basic protection\n\n"
                "**Balanced:**\n"
                "`balanced` - Good protection, low impact\n"
                "`medium` - More features\n"
                "`standard` - Recommended\n\n"
                "**Security Focused:**\n"
                "`maximum` - VM + full protection\n"
                "`ultra` - All features"
            ),
            ephemeral=True
        )
    
    @ui.button(label="Reset", style=discord.ButtonStyle.gray, emoji="🔄", row=3)
    async def reset_button(self, interaction: discord.Interaction, button: ui.Button):
        user_id = interaction.user.id
        user_configs[user_id] = obf.get_default_config()
        
        await interaction.response.send_message("✅ Configuration reset!", ephemeral=True)
    
    @ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="❌", row=3)
    async def cancel_button(self, interaction: discord.Interaction, button: ui.Button):
        user_id = interaction.user.id
        if user_id in user_configs:
            del user_configs[user_id]
        if user_id in user_code:
            del user_code[user_id]
        
        await interaction.response.edit_message(
            embed=embed("❌ Cancelled", "Custom configuration cancelled."),
            view=None
        )


class PresetView(ui.View):
    """Quick preset selection view"""
    
    def __init__(self):
        super().__init__(timeout=60)
    
    @ui.button(label="Mobile/Delta", style=discord.ButtonStyle.gray, emoji="📱")
    async def mobile_btn(self, interaction: discord.Interaction, button: ui.Button):
        await self._apply_preset(interaction, 'mobile')
    
    @ui.button(label="Light", style=discord.ButtonStyle.green, emoji="💨")
    async def light_btn(self, interaction: discord.Interaction, button: ui.Button):
        await self._apply_preset(interaction, 'light')
    
    @ui.button(label="Balanced", style=discord.ButtonStyle.blurple, emoji="⚖️")
    async def balanced_btn(self, interaction: discord.Interaction, button: ui.Button):
        await self._apply_preset(interaction, 'balanced')
    
    @ui.button(label="Standard", style=discord.ButtonStyle.blurple, emoji="🛡️")
    async def standard_btn(self, interaction: discord.Interaction, button: ui.Button):
        await self._apply_preset(interaction, 'standard')
    
    @ui.button(label="Maximum", style=discord.ButtonStyle.red, emoji="🔐")
    async def maximum_btn(self, interaction: discord.Interaction, button: ui.Button):
        await self._apply_preset(interaction, 'maximum')
    
    async def _apply_preset(self, interaction: discord.Interaction, preset: str):
        user_id = interaction.user.id
        code = user_code.get(user_id)
        
        if not code:
            await interaction.response.send_message("❌ No code found!", ephemeral=True)
            return
        
        await interaction.response.defer()
        
        try:
            result, stats = obf.obfuscate(code, level=preset)
            
            file = discord.File(io.BytesIO(result.encode('utf-8')), filename=f'{preset}_protected.lua')
            
            e = embed(f"✅ {preset.upper()} Protection Complete!", "", C.GREEN)
            e.add_field(name="📊 Stats", value=f"```\nSize: {stats['original_size']} → {stats['obfuscated_size']} bytes\nScore: {stats['protection_score']}```", inline=False)
            
            await interaction.followup.send(embed=e, file=file)
            
            if user_id in user_code:
                del user_code[user_id]
                
        except Exception as ex:
            await interaction.followup.send(embed=embed("❌ Error", str(ex), C.RED))


# ==================== BOT EVENTS ====================

@bot.event
async def on_ready():
    print(f"[+] Bot ready: {bot.user}")
    print(f"[+] Servers: {len(bot.guilds)}")
    await bot.change_presence(activity=discord.Game("!help | LuaShield Pro v2.1"))
    try:
        await bot.tree.sync()
        print("[+] Slash commands synced")
    except Exception as e:
        print(f"[-] Sync error: {e}")


# ==================== COMMANDS ====================

@bot.command(name='help', aliases=['h', 'menu'])
async def help_cmd(ctx):
    e = embed("🔒 LuaShield Pro v2.1", "Professional Lua Obfuscator\nOptimized for Roblox Executors")
    
    e.add_field(
        name="📋 Commands",
        value="""
`!obf [level]` - Quick obfuscate
`!custom` - Custom configuration
`!presets` - Show all presets
`!compare` - Compare presets
`!ping` - Bot latency
        """,
        inline=True
    )
    
    e.add_field(
        name="🎚️ Quick Levels",
        value="""
`mobile` - For weak executors
`delta` - Delta optimized
`light` - Fast & basic
`balanced` - Recommended
`standard` - Full protection
`maximum` - VM included
        """,
        inline=True
    )
    
    e.add_field(
        name="📤 Usage",
        value="1. Upload `.lua` file\n2. Use `!obf level` or `!custom`\n\nOr use code block with command",
        inline=False
    )
    
    await ctx.send(embed=e)


@bot.command(name='presets', aliases=['levels', 'lvl'])
async def presets_cmd(ctx):
    e = embed("📋 Protection Presets")
    
    presets = [
        ("📱 Mobile", "mobile", "Minimal protection for weak/mobile executors\n`CPU: None` `Size: Minimal`"),
        ("📱 Delta", "delta", "Optimized for Delta executor\n`CPU: Very Low` `Size: Low`"),
        ("💨 Light", "light", "Fast, basic encryption\n`CPU: Very Low` `Size: Low`"),
        ("⚖️ Balanced", "balanced", "Good protection, low impact\n`CPU: Low` `Size: Low`"),
        ("🛡️ Standard", "standard", "Recommended for most scripts\n`CPU: Medium` `Size: Medium`"),
        ("🔐 Maximum", "maximum", "VM + full protection\n`CPU: High` `Size: High`"),
        ("💎 Ultra", "ultra", "All features enabled\n`CPU: Very High` `Size: Very High`"),
    ]
    
    for name, cmd, desc in presets:
        e.add_field(name=f"{name} (`{cmd}`)", value=desc, inline=True)
    
    e.add_field(
        name="💡 Tip",
        value="Use `!custom` for fine-grained control over each feature!",
        inline=False
    )
    
    await ctx.send(embed=e)


@bot.command(name='compare')
async def compare_cmd(ctx):
    """Compare preset features"""
    e = embed("📊 Preset Comparison")
    
    features = ['string_encryption', 'variable_rename', 'control_flow', 'junk_code', 'anti_tamper', 'virtualization']
    presets_to_show = ['mobile', 'light', 'balanced', 'standard', 'maximum']
    
    header = "Feature        |" + "|".join([p[:3].upper() for p in presets_to_show])
    lines = [header, "-" * len(header)]
    
    emoji_map = {True: "✅", False: "❌"}
    
    for feat in features:
        feat_name = feat.replace('_', ' ')[:14].ljust(14)
        values = [emoji_map[obf.PRESETS[p].get(feat, False)] for p in presets_to_show]
        lines.append(f"{feat_name} |" + " | ".join(values))
    
    e.description = f"```\n" + "\n".join(lines) + "\n```"
    
    e.add_field(
        name="📈 Performance Impact",
        value="Mobile < Light < Balanced < Standard < Maximum < Ultra",
        inline=False
    )
    
    await ctx.send(embed=e)


@bot.command(name='custom', aliases=['c', 'configure'])
async def custom_cmd(ctx):
    """Open custom configuration panel"""
    
    # Get code from attachment or code block
    code = None
    
    if ctx.message.attachments:
        att = ctx.message.attachments[0]
        if att.filename.endswith(('.lua', '.txt')):
            try:
                code = (await att.read()).decode('utf-8')
            except:
                pass
    
    if not code:
        match = re.search(r'```(?:lua)?\s*([\s\S]+?)```', ctx.message.content)
        if match:
            code = match.group(1).strip()
    
    if not code:
        e = embed("🎛️ Custom Mode", 
            "**How to use:**\n\n"
            "1️⃣ Upload a `.lua` file with this command\n"
            "2️⃣ Or use a code block:\n"
            "```\n!custom\n```lua\nyour code\n```\n```\n\n"
            "3️⃣ Select features you want\n"
            "4️⃣ Click 'Apply & Obfuscate'",
            C.YELLOW
        )
        await ctx.send(embed=e)
        return
    
    # Store code for this user
    user_code[ctx.author.id] = code
    user_configs[ctx.author.id] = obf.get_default_config()
    
    # Show configuration panel
    e = embed("🎛️ Custom Configuration", 
        f"**Code loaded:** {len(code)} bytes\n\n"
        "Select the features you want below.\n"
        "Use the dropdowns to configure, then click **Apply & Obfuscate**."
    )
    
    e.add_field(
        name="💡 Tips",
        value="• For Delta/Mobile: Only select String Encryption + Variable Rename\n"
              "• For balanced: Add Control Flow + Anti-Tamper\n"
              "• Avoid VM Protection for weak executors",
        inline=False
    )
    
    view = CustomView(code)
    await ctx.send(embed=e, view=view)


@bot.command(name='quick', aliases=['q'])
async def quick_cmd(ctx):
    """Quick preset selection with buttons"""
    
    code = None
    
    if ctx.message.attachments:
        att = ctx.message.attachments[0]
        if att.filename.endswith(('.lua', '.txt')):
            try:
                code = (await att.read()).decode('utf-8')
            except:
                pass
    
    if not code:
        match = re.search(r'```(?:lua)?\s*([\s\S]+?)```', ctx.message.content)
        if match:
            code = match.group(1).strip()
    
    if not code:
        await ctx.send(embed=embed("❌ No Code", "Upload a file or use code block!", C.RED))
        return
    
    user_code[ctx.author.id] = code
    
    e = embed("⚡ Quick Obfuscate", f"**Code loaded:** {len(code)} bytes\n\nSelect a preset:")
    await ctx.send(embed=e, view=PresetView())


@bot.command(name='ping')
async def ping_cmd(ctx):
    await ctx.send(embed=embed("🏓 Pong!", f"Latency: {round(bot.latency*1000)}ms"))


@bot.command(name='obfuscate', aliases=['obf', 'o', 'protect'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def obf_cmd(ctx, level: str = "balanced"):
    """Main obfuscate command with preset"""
    
    # All available presets
    all_presets = list(obf.PRESETS.keys())
    
    if level.lower() not in all_presets:
        suggestions = ", ".join([f"`{p}`" for p in all_presets])
        e = embed("⚠️ Unknown Preset", f"Available: {suggestions}\n\nUsing `balanced`", C.YELLOW)
        await ctx.send(embed=e)
        level = "balanced"
    
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
                await ctx.send(embed=embed("❌ Error", "Cannot read file", C.RED))
                return
    
    if not code:
        match = re.search(r'```(?:lua)?\s*([\s\S]+?)```', ctx.message.content)
        if match:
            code = match.group(1).strip()
    
    if not code:
        e = embed("📝 Usage", 
            f"**Upload `.lua` file** with `!obf {level}`\n\n"
            "**Or use code block:**\n"
            f"```\n!obf {level}\n```lua\nyour code\n```\n```\n\n"
            "**Quick commands:**\n"
            "`!custom` - Choose individual features\n"
            "`!quick` - Quick preset buttons\n"
            "`!presets` - See all presets",
            C.YELLOW
        )
        await ctx.send(embed=e)
        return
    
    if len(code) > 200000:
        await ctx.send(embed=embed("❌ Too Large", "Maximum 200KB", C.RED))
        return
    
    # Show impact warning for heavy presets
    if level in ['maximum', 'ultra']:
        impact = obf.estimate_impact(obf.PRESETS[level])
        e = embed("⚠️ Heavy Protection", 
            f"**{level.upper()}** may cause lag on weak executors.\n\n"
            f"**CPU Impact:** {impact['cpu_label']}\n"
            f"**Recommended for:** {impact['recommended_for']}\n\n"
            "Consider `balanced` or `delta` for mobile/weak executors.",
            C.YELLOW
        )
        await ctx.send(embed=e)
    
    # Process
    msg = await ctx.send(embed=embed("⏳ Processing...", f"Level: **{level.upper()}**", C.YELLOW))
    
    try:
        result, stats = obf.obfuscate(code, level=level.lower())
        
        out_name = filename.rsplit('.', 1)[0] + f'_{level}_protected.lua'
        file = discord.File(io.BytesIO(result.encode('utf-8')), filename=out_name)
        
        e = embed("✅ Protection Complete!", f"Level: **{level.upper()}**", C.GREEN)
        e.add_field(
            name="📊 Statistics",
            value=f"```\nOriginal:  {stats['original_size']:,} bytes\nProtected: {stats['obfuscated_size']:,} bytes\nIncrease:  {stats['size_increase']}\nTime:      {stats['processing_time']}\nScore:     {stats['protection_score']}```",
            inline=False
        )
        e.add_field(
            name="🛡️ Layers",
            value="• " + "\n• ".join(stats['layers_applied']),
            inline=True
        )
        e.add_field(
            name="🔑 ID",
            value=f"`{stats['watermark']}`",
            inline=True
        )
        
        await msg.edit(embed=e)
        await ctx.send(file=file)
        
    except Exception as ex:
        await msg.edit(embed=embed("❌ Error", str(ex), C.RED))


@obf_cmd.error
async def obf_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=embed("⏳ Cooldown", f"Wait {error.retry_after:.1f}s", C.YELLOW))


# ==================== SLASH COMMANDS ====================

@bot.tree.command(name="obfuscate", description="Protect your Lua script")
@app_commands.describe(
    level="Protection level preset",
    code="Lua code (optional if uploading file)"
)
@app_commands.choices(level=[
    app_commands.Choice(name="📱 Mobile (Weakest)", value="mobile"),
    app_commands.Choice(name="📱 Delta Optimized", value="delta"),
    app_commands.Choice(name="💨 Light", value="light"),
    app_commands.Choice(name="⚖️ Balanced (Recommended)", value="balanced"),
    app_commands.Choice(name="🛡️ Standard", value="standard"),
    app_commands.Choice(name="🔐 Maximum (Heavy)", value="maximum"),
    app_commands.Choice(name="💎 Ultra (Heaviest)", value="ultra"),
])
async def slash_obf(interaction: discord.Interaction, level: str = "balanced", code: str = None):
    await interaction.response.defer()
    
    if not code:
        await interaction.followup.send(embed=embed("📝 No Code", "Provide code in the `code` parameter", C.YELLOW))
        return
    
    try:
        result, stats = obf.obfuscate(code, level=level)
        file = discord.File(io.BytesIO(result.encode('utf-8')), filename='protected.lua')
        
        e = embed("✅ Protected!", f"Level: **{level.upper()}** | Score: {stats['protection_score']}", C.GREEN)
        await interaction.followup.send(embed=e, file=file)
        
    except Exception as ex:
        await interaction.followup.send(embed=embed("❌ Error", str(ex), C.RED))


# ==================== RUN ====================

def run_bot():
    if TOKEN == 'YOUR_TOKEN':
        print("[-] Set DISCORD_TOKEN in environment/secrets!")
        return
    bot.run(TOKEN)

if __name__ == '__main__':
    run_bot()