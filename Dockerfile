# Sử dụng image Python nhẹ
FROM python:3.14-slim

# Đặt biến môi trường để tránh tạo file .pyc và đảm bảo stdout/stderr được ghi ngay lập tức
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Tạo folder secrets để Cloud Run có thể mount file cookies vào
RUN mkdir -p /secrets

# Expose cổng chạy FastAPI (mặc định 8000)
EXPOSE 8000

# Chạy ứng dụng với uvicorn
CMD ["python", "main.py"]
