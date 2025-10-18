import asyncio

import uvicorn
from fastapi import FastAPI, HTTPException

from core.config import DISCORD_TOKEN
from services.discord_bot import bot
from services.convert_yt import download_and_extract_audio
from pydantic import BaseModel

app = FastAPI()

class ConvertRequest(BaseModel):
    url: str
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/")
async def convert(req: ConvertRequest):
    try:
        download_and_extract_audio(req.url)
        return {"url": req.url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"⚠️ Đã xảy ra lỗi: {e}")
        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=400, detail=f"Lỗi xử lý: {str(e)}")

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
