import discord
from discord.ext import commands

from core.config import DISCORD_GUILD_ID

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    guild = discord.Object(id=int(DISCORD_GUILD_ID))
    synced = await bot.tree.sync()
    await  bot.tree.sync(guild=guild)
    print(f"✅ Logged in as {bot.user}")
    print(f"🔁 Synced {len(synced)} commands:")
    for cmd in synced:
        print(f" • /{cmd.name}")

async def load_commands():
    await bot.load_extension("commands.get_audio")
    print("✅ Loaded command: get_audio")
    await bot.load_extension("commands.qr_bank")
    print("✅ Loaded command: qr_bank")