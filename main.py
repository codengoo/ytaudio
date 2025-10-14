from services.discord_bot import bot
from core.config import DISCORD_TOKEN

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)