import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.config import HOST_URL, OUTPUT_URL
from services.convert_yt import download_and_extract_audio, getInfo

router = APIRouter()

class ConvertRequest(BaseModel):
    url: str

@router.post("/")
async def convert(req: ConvertRequest):
    try:
        audio_path = download_and_extract_audio(req.url)
        file_name = os.path.basename(audio_path)
        return {"url": req.url, "link": f"{HOST_URL}/{OUTPUT_URL}/{file_name}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Lỗi xử lý: {str(e)}")

@router.get("/")
async def info(url: str):
    try:
        video_id, title = getInfo(url)
        return {"id": video_id, "title": title}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Lỗi xử lý: {str(e)}")