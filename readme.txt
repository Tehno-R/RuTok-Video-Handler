Пример .env файла:
##########################################################
INPUT_PATH="input_video/"
OUTPUT_PATH="output_video/"
FFMPEG_BINARY_PATH="ffmpeg/bin/ffmpeg.exe"
FFPROBE_BINARY_PATH="ffmpeg/bin/ffprobe.exe"

FAST_API_PORT=8000
UPLOAD_VIDEO_URL="http://localhost:10003/api/files/upload"
##########################################################

Что нужно для запуска:
.env файл в директории проекта со всеми переменными
бинарные файлы FFmpeg и FFprobe (в .env прописать пути до файлов)
Запустить App/main.py
