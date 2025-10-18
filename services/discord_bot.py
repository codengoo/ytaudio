import discord
from discord.ext import commands

from core.config import DISCORD_GUILD_ID

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.tree.command(name="get_audio", description="Tải audio từ youtube")
async def get_audio(interaction: discord.Interaction, url: str):
    await interaction.response.send_message(f"Getting from {url}")

@bot.tree.command(name="info", description="Thông tin Youtube")
async def get_info(interaction: discord.Interaction, url: str):
    await interaction.response.send_message(f"Getting from {url}")

@bot.event
async def on_ready():
    guild = discord.Object(id=int(DISCORD_GUILD_ID))
    synced = await bot.tree.sync()
    await  bot.tree.sync(guild=guild)
    print(f"✅ Logged in as {bot.user}")
    print(f"🔁 Synced {len(synced)} commands:")
    for cmd in synced:
        print(f" • /{cmd.name}")
