import os

import discord
from discord.ext import commands

from core.config import DISCORD_GUILD_ID, HOST_URL, OUTPUT_URL
from services.convert_yt import getInfo, download_and_extract_audio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)


class DownloadButton(discord.ui.View):
    def __init__(self, youtube_url: str, title: str):
        super().__init__(timeout=None)  # Không auto xoá view
        self.youtube_url = youtube_url
        self.title = title

    @discord.ui.button(
        label="🎧 Download Audio",
        style=discord.ButtonStyle.green,
        custom_id="download_audio"
    )
    async def download_audio_button(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        try:
            audio_path = download_and_extract_audio(self.youtube_url)
            file_name = os.path.basename(audio_path)
            link = f"{HOST_URL}/{OUTPUT_URL}/{file_name}"

            # Gửi kết quả
            await interaction.followup.send(
                f"✅ Tải về tại đây: [{self.title}]({link})"
            )

        except Exception as e:
            await interaction.followup.send(f"⚠️ Lỗi khi tải audio: {str(e)}", ephemeral=True)


@bot.tree.command(name="get_audio", description="Tải audio từ youtube")
async def get_audio(interaction: discord.Interaction, url: str):
    await interaction.response.defer()  # Cho Discord biết bot đang xử lý

    try:
        # Gọi hàm lấy thông tin video (giả sử bạn đã có)
        video_id, title = getInfo(url)
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        video_link = f"https://www.youtube.com/watch?v={video_id}"

        # Tạo embed hiển thị thông tin video
        embed = discord.Embed(
            title=title,
            url=video_link,
            description=f"🎵 **Video ID:** `{video_id}`",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_footer(text="YouTube Audio Downloader")

        # Tạo button "Download Audio"
        view = DownloadButton(youtube_url=url, title=title)
        await interaction.followup.send(embed=embed, view=view)

    except Exception as e:
        await interaction.followup.send(f"⚠️ Lỗi khi xử lý URL: {str(e)}", ephemeral=True)


@bot.event
async def on_ready():
    guild = discord.Object(id=int(DISCORD_GUILD_ID))
    synced = await bot.tree.sync()
    await  bot.tree.sync(guild=guild)
    print(f"✅ Logged in as {bot.user}")
    print(f"🔁 Synced {len(synced)} commands:")
    for cmd in synced:
        print(f" • /{cmd.name}")
