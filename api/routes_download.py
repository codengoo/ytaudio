from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
import os

from core.config import OUTPUT_DIR

router = APIRouter()

@router.get("/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    # Trả file kèm header buộc tải
    return FileResponse(
        path=file_path,
        filename=filename,  # Tên file khi tải về
        media_type="application/octet-stream"  # Ép tải
    )
