from dotenv import load_dotenv
import os
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")

OUTPUT_DIR="downloads"
OUTPUT_URL="export"
HOST_URL=f"http://localhost:8000"