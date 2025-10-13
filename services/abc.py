import os
import re
import yt_dlp
from moviepy import VideoFileClip

# Chỉ định đường dẫn tuyệt đối đến ffmpeg.exe
ffmpeg_path = r"D:\WORK\pet\ytaudio\ffmpeg\bin\ffmpeg.exe"  # Đảm bảo đường dẫn chính xác
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

def download_and_extract_audio(youtube_url, output_dir="downloads"):
    try:
        # Kiểm tra URL hợp lệ
        if not youtube_url.startswith("https://www.youtube.com/watch?v="):
            raise ValueError(
                "URL không hợp lệ. Vui lòng nhập URL YouTube hợp lệ (bắt đầu bằng https://www.youtube.com/watch?v=)")

        # Tạo thư mục output nếu chưa tồn tại
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Cấu hình yt-dlp để tải video
        ydl_opts = {
            'format': 'best',  # Tải chất lượng tốt nhất
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Tên file dựa trên tiêu đề video
            'noplaylist': True,  # Không tải playlist
            'ffmpeg_location': ffmpeg_path,  # Chỉ định ffmpeg cho yt-dlp
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Tải video và lấy thông tin
            info = ydl.extract_info(youtube_url, download=True)
            title = info.get('title', 'unknown')

            # Làm sạch tiêu đề để tạo tên file an toàn
            safe_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_').lower()
            video_filename = f"{safe_title}.mp4"
            audio_filename = f"{safe_title}.mp3"

            # Đổi tên file video tải về thành tên an toàn
            original_video_file = ydl.prepare_filename(info).replace('.webm', '.mp4').replace('.mkv', '.mp4')
            video_file = os.path.join(output_dir, video_filename)
            if os.path.exists(original_video_file):
                os.rename(original_video_file, video_file)

            print(f"Đã tải video: {title} (lưu tại: {video_file})")

        # Trích xuất audio từ file video
        video_clip = VideoFileClip(video_file)
        audio_file = os.path.join(output_dir, audio_filename)
        video_clip.audio.write_audiofile(audio_file)

        # Đóng clip để giải phóng bộ nhớ
        video_clip.close()

        # Xóa file video tạm
        if os.path.exists(video_file):
            os.remove(video_file)

        print(f"Đã trích xuất audio: {audio_file}")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        import traceback
        traceback.print_exc()


# Sử dụng: Thay URL bằng link YouTube của bạn
if __name__ == "__main__":
    # url = "https://www.youtube.com/watch?v=lkT6NMB5-Jg"
    url = "https://www.youtube.com/watch?v=Edrw9A1Zdxk"
    download_and_extract_audio(url)
