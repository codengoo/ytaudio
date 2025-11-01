import os
import re
from typing import Tuple

from moviepy import VideoFileClip
from yt_dlp import YoutubeDL

from core.config import OUTPUT_DIR, FFMPEG_PATH
from utils.gcs import upload_to_gcs, make_public_url

# --- Cấu hình ---
os.environ["IMAGEIO_FFMPEG_EXE"] = FFMPEG_PATH  # MoviePy dùng ffmpeg này

# ==========================
# 🔹 1. Hàm kiểm tra URL YouTube
# ==========================
def check_youtube_url_pattern(url: str) -> bool:
    """Kiểm tra xem URL có đúng định dạng video YouTube không."""
    pattern = re.compile(
        r'^(https?://)?(www\.)?'
        r'(youtube\.com/watch\?v=|youtu\.be/)'
        r'([\w-]{11})'
    )
    return bool(pattern.match(url))


def check_youtube_url_exists(url: str) -> bool:
    """Kiểm tra xem video YouTube có tồn tại thực tế không (bằng yt_dlp)."""
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return bool(info and info.get("id") and info.get("title"))
    except Exception:
        return False


def is_url_valid(url: str) -> bool:
    """Kết hợp kiểm tra định dạng và tồn tại."""
    return check_youtube_url_pattern(url) and check_youtube_url_exists(url)

# ==========================
# 🔹 2. Xử lý tên file
# ==========================
def clean_file_name(file_name: str) -> Tuple[str, str]:
    """Tạo tên file an toàn cho video và audio."""
    safe_title = re.sub(r'[^\w\s-]', '', file_name).replace(' ', '_').lower()
    video_filename = f"{safe_title}.mp4"
    audio_filename = f"{safe_title}.mp3"
    return video_filename, audio_filename

# ==========================
# 🔹 3. Tải video
# ==========================
def download_video(youtube_url: str) -> str:
    cookie_path = "/secrets/cookies.txt"
    """Tải video từ YouTube và trả về đường dẫn file video."""
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(OUTPUT_DIR, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'ffmpeg_location': FFMPEG_PATH,
    }

    # 🔹 Nếu file cookie tồn tại, thêm vào config
    if os.path.exists(cookie_path):
        print(f"✅ Sử dụng cookie từ {cookie_path}")
        ydl_opts['cookiefile'] = cookie_path
    else:
        print("⚠️ Không tìm thấy cookies.txt — có thể bị hạn chế tải một số video YouTube")

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        title = info.get('title', 'unknown')

        # Đổi tên file cho an toàn
        video_filename, _ = clean_file_name(title)
        original_file = ydl.prepare_filename(info).replace('.webm', '.mp4').replace('.mkv', '.mp4')
        new_path = os.path.join(OUTPUT_DIR, video_filename)

        if os.path.exists(original_file):
            os.rename(original_file, new_path)

        print(f"✅ Đã tải video: {title}\n📁 Lưu tại: {new_path}")
        return new_path

# ==========================
# 🔹 4. Chuyển đổi sang audio (MP3)
# ==========================
def convert_to_audio(video_file: str) -> str:
    """Trích xuất audio từ video (MP4 → MP3)."""
    video_clip = VideoFileClip(video_file)
    base_name = os.path.splitext(os.path.basename(video_file))[0]
    audio_file = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")

    video_clip.audio.write_audiofile(audio_file)
    video_clip.close()

    # Xóa video tạm
    if os.path.exists(video_file):
        os.remove(video_file)

    print(f"🎵 Đã trích xuất audio: {audio_file}")
    return audio_file

# ==========================
# 🔹 5. Quy trình tổng hợp
# ==========================
def download_and_extract_audio(youtube_url: str):
    """Quy trình: kiểm tra, tải video và trích xuất audio."""
    # Kiểm tra URL hợp lệ
    if not is_url_valid(youtube_url):
        raise ValueError("❌ URL không hợp lệ hoặc video không tồn tại.")

    # Tạo thư mục output
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Tải video và trích xuất audio
    video_path = download_video(youtube_url)
    audio_path = convert_to_audio(video_path)

    # 2️⃣ Upload lên GCS
    base_name = os.path.basename(audio_path)
    dest_path = f"audios/{base_name}"
    upload_to_gcs(audio_path, dest_path)

    # 3️⃣ Tạo link tải (chọn 1 trong 2 cách)
    download_url = make_public_url(dest_path)

    print(f"✅ Hoàn tất! Audio được lưu tại: {download_url}")
    return audio_path

def getInfo(youtube_url:str)->Tuple[str, str]:
    # Kiểm tra URL hợp lệ
    if not is_url_valid(youtube_url):
        raise ValueError("❌ URL không hợp lệ hoặc video không tồn tại.")

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info["id"], info["title"]
