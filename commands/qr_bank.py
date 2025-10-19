import discord
from discord import app_commands
from discord.ext import commands

from services.bank_qr import get_bank_qr_discord_id


# Slash command
@app_commands.command(name="qr_bank", description="Lấy mã QR chuyển khoản của một người dùng")
@app_commands.describe(user="Chọn người dùng trong server")
async def get_qr_bank(interaction: discord.Interaction, user: discord.User):
    await interaction.response.defer(thinking=True, ephemeral=True)

    try:
        qr_url = get_bank_qr_discord_id(user.id)
        embed = discord.Embed(
            title="💳 Mã QR chuyển khoản",
            description=f"QR dành cho ID: `{user.id}`",
            color=discord.Color.green()
        )
        embed.set_image(url=qr_url)
        embed.set_footer(text="Dùng app ngân hàng quét mã để chuyển khoản")

        await interaction.followup.send(embed=embed, ephemeral=True)

    except Exception as e:
        await interaction.followup.send(
            f"⚠️ Lỗi khi tạo mã QR: `{str(e)}`",
            ephemeral=True
        )


# ⚙️ Setup để load command
async def setup(bot: commands.Bot):
    bot.tree.add_command(get_qr_bank)
