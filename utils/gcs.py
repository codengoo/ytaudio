import os
from google.cloud import storage
from datetime import timedelta

# 🟢 Lấy tên bucket từ biến môi trường
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "your-bucket-name")

# 🟢 Hàm khởi tạo client
def get_storage_client():
    return storage.Client()

# ==============================
# 🔹 1. Upload file lên GCS
# ==============================
def upload_to_gcs(local_path: str, dest_path: str) -> str:
    """
    Upload file lên GCS.
    Args:
        local_path: đường dẫn file local
        dest_path: đường dẫn trong bucket (ví dụ: "audios/file.mp3")
    Returns:
        Đường dẫn GCS (gs://...)
    """
    client = get_storage_client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(dest_path)

    blob.upload_from_filename(local_path)

    print(f"✅ Uploaded {local_path} → gs://{GCS_BUCKET_NAME}/{dest_path}")
    return f"gs://{GCS_BUCKET_NAME}/{dest_path}"

# ==============================
# 🔹 2. Tạo public URL
# ==============================
def make_public_url(dest_path: str) -> str:
    """Trả về URL công khai của object (nếu bucket public)."""
    return f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{dest_path}"

# ==============================
# 🔹 3. Tạo signed URL (tùy chọn)
# ==============================
def generate_signed_url(dest_path: str, expires_minutes: int = 60) -> str:
    """Tạo signed URL tạm thời để tải file."""
    client = get_storage_client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(dest_path)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expires_minutes),
        method="GET",
    )
    return url
