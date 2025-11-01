from dotenv import load_dotenv
import os
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")
FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")
HOST_URL=os.getenv("HOST_URL", f"http://localhost:8000")

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "download")
OUTPUT_URL="export"