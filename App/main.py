import os
import sys
import threading

from pydantic import BaseModel

import Logger

import httpx
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, HTTPException

from controllers.path_controller import PathHandler
from ffmpeg_handler import FFmpegHandler
from controllers.id_controller import IdController

from core.domain import Video

logger = Logger.generate_logger("App")
PathHandler.load_env_variables()
FAST_API_PORT=os.getenv("FAST_API_PORT")
UPLOAD_VIDEO_URL=os.getenv("UPLOAD_VIDEO_URL")


VIDEO_FILE_EXTENSIONS_MEDIATYPE = {
        'mp4': 'video/mp4',
        'webm': 'video/webm',
        'mov': 'video/quicktime'
    }

@asynccontextmanager
async def lifespan(application: FastAPI):
    PathHandler.refresh_paths(refresh_directories=True)
    yield # разделитель между "до запуска" и "после завершения" (обязательно должен присутствовать в функции (хз почему))

app = FastAPI(lifespan=lifespan)

responses = {
    500: {},
    200: {}
}
@app.post("/api/files/handle", responses=responses)
async def get_file(uploaded_file: UploadFile):
    try:
        logger.info("Endpoint '/api/files/handle' called")
        file = uploaded_file.file
        filename = uploaded_file.filename
        uniq_id = IdController.generate_unique_id()
        video = Video(filename, uniq_id)
        save_path = PathHandler.get_input_path().joinpath(uniq_id)
        with open(save_path, "wb") as f:
            f.write(file.read())
        threading.Thread(target=handle_video, args=(video,), daemon=False).start()
    except Exception as e:
        logger.error("Endpoint '/api/files/handle' failed", exc_info=e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_media_type(filename: str) -> str:
    ext = filename.split('.')[-1].lower()
    return VIDEO_FILE_EXTENSIONS_MEDIATYPE.get(ext, 'application/octet-stream')

def handle_video(video: Video):
    logger.info(f"Starting video handle process with {video.get_uid_name()} ({video.get_origin_name()})")
    FFmpegHandler(video=video)
    PathHandler.delete_file_from_input(video=video)
    send_video(video=video)
    PathHandler.delete_file_from_output(video=video)
    IdController.delete_unique_id(video.get_uid_name())
    logger.info(f"Finished video handle process with {video.get_uid_name()}")

def send_video(video: Video):
    url = UPLOAD_VIDEO_URL
    files = {
        'file': (video.get_origin_name(),
                 open(PathHandler.get_output_path().joinpath(video.get_uid_name()), 'rb'),
                 'video/mp4')
    }
    try:
        httpx.post(url, files=files)
    except httpx.HTTPError as e:
        logger.error(f"Error sending video file {video.get_uid_name()} to service storage video")
    else:
        logger.info(f"Video file {video.get_uid_name()} sent to service storage video")

if __name__ == "__main__":
    try:
        port = int(FAST_API_PORT)
    except ValueError:
        logger.critical("FAST_API_PORT environment variable is not set or is not int")
        sys.exit(1)
    else:
        logger.info("Starting uvicorn server")
        uvicorn.run("main:app", host="localhost", port=port)
