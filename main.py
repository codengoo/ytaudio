import asyncio
import os

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from api.routes_convert import router as convert_router
from api.routes_default import router as default_router
from core.config import DISCORD_TOKEN, OUTPUT_DIR, OUTPUT_URL
from services.discord_bot import bot

app = FastAPI()

# Static
os.makedirs(OUTPUT_DIR, exist_ok=True)
app.mount(f"/{OUTPUT_URL}", StaticFiles(directory=OUTPUT_DIR), name=OUTPUT_URL)

# Routes
app.include_router(convert_router, prefix="/convert", tags=["convert"])
app.include_router(default_router, tags=["convert"])


async def start_bot():
    print("🚀 Starting bot...")
    await bot.start(DISCORD_TOKEN)


async def start_server():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await  asyncio.gather(start_bot(), start_server())


if __name__ == "__main__":
    asyncio.run(main())
