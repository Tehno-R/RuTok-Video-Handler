FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH="src:src/controllers:src/domain:src/frameworks"

ENV INPUT_PATH="input_video/"
ENV OUTPUT_PATH="output_video/"
ENV FFMPEG_BINARY_PATH="ffmpeg_linux/ffmpeg"
ENV FFPROBE_BINARY_PATH="ffmpeg_linux/ffprobe"
ENV FAST_API_PORT=8000
ENV UPLOAD_VIDEO_URL="http://api:8001/api/files/upload"

# Копируем ВСЕ файлы проекта, включая кастомные пакеты
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]