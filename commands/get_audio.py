import os
import discord
from discord import app_commands
from discord.ext import commands

from core.config import HOST_URL, OUTPUT_URL
from services.convert_yt import getInfo, download_and_extract_audio


class DownloadButton(discord.ui.View):
    def __init__(self, youtube_url: str, title: str):
        super().__init__(timeout=None)
        self.youtube_url = youtube_url
        self.title = title

    @discord.ui.button(
        label="🎧 Download Audio",
        style=discord.ButtonStyle.green,
        custom_id="download_audio"
    )
    async def download_audio_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=True)

        try:
            audio_path = download_and_extract_audio(self.youtube_url)
            file_name = os.path.basename(audio_path)
            link = f"{HOST_URL}/{OUTPUT_URL}/{file_name}"

            await interaction.followup.send(
                f"✅ Tải về tại đây: [{self.title}]({link})"
            )
        except Exception as e:
            await interaction.followup.send(f"⚠️ Lỗi khi tải audio: {str(e)}", ephemeral=True)


# Slash command
@app_commands.command(name="get_audio", description="Tải audio từ YouTube")
async def get_audio(interaction: discord.Interaction, url: str):
    await interaction.response.defer()

    try:
        video_id, title = getInfo(url)
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        video_link = f"https://www.youtube.com/watch?v={video_id}"

        embed = discord.Embed(
            title=title,
            url=video_link,
            description=f"🎵 **Video ID:** `{video_id}`",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_footer(text="YouTube Audio Downloader")

        view = DownloadButton(youtube_url=url, title=title)
        await interaction.followup.send(embed=embed, view=view)

    except Exception as e:
        await interaction.followup.send(f"⚠️ Lỗi khi xử lý URL: {str(e)}", ephemeral=True)


# Hàm setup để load command này
async def setup(bot: commands.Bot):
    bot.tree.add_command(get_audio)
