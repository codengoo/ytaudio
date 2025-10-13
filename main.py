import uvicorn
from fastapi import FastAPI
from services.discord_bot import bot
from core.config import DISCORD_TOKEN
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def on_startup():
    await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)