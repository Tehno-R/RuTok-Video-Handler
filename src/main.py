import os
import sys
import threading
from contextlib import asynccontextmanager

import httpx
import dotenv
dotenv.load_dotenv()
import uvicorn
from fastapi import FastAPI, UploadFile, HTTPException

import Logger
logger = Logger.generate_logger("App")
from controllers.id_controller import IdController
from controllers.path_controller import PathHandler
from domain.video import Video
from frameworks.ffmpeg_handler import FFmpegHandler


VIDEO_FILE_EXTENSIONS_MEDIATYPE = {
        'mp4': 'video/mp4',
        'webm': 'video/webm',
        'mov': 'video/quicktime'
    }

UPLOAD_VIDEO_URL = os.getenv("UPLOAD_VIDEO_URL")

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
    handler = FFmpegHandler(video=video)
    status_code = handler.to_handle()
    if status_code != 0:
        logger.error(f"Handling video file {video.get_uid_name()} finished with error")
        PathHandler.delete_file_from_input(video=video)
        PathHandler.delete_file_from_output(video=video)
        return
    PathHandler.delete_file_from_input(video=video)
    send_video(video=video)
    PathHandler.delete_file_from_output(video=video)
    IdController.delete_unique_id(video.get_uid_name())
    logger.info(f"Finished video handle process with {video.get_uid_name()}")

def send_video(video: Video):
    with (open(PathHandler.get_output_path().joinpath(video.get_uid_name()), 'rb') as video_file,
          open(PathHandler.get_output_path().joinpath(video.get_uid_name().__str__() + "_preview"), 'rb') as photo_file):
        files = {
            'file': (video.get_origin_name(), video_file, 'video/mp4'),
            'preview': (video.get_origin_name_for_preview(), photo_file, 'image/jpeg')
        }

        try:
            httpx.post(UPLOAD_VIDEO_URL, files=files)
        except httpx.HTTPError as e:
            logger.error(f"Error sending video file {video.get_uid_name()} to service storage video {UPLOAD_VIDEO_URL}")
        else:
            logger.info(f"Video file {video.get_uid_name()} sent to service storage video")

if __name__ == "__main__":
    # print(os.getenv("PYTHONPATH"))
    FAST_API_PORT = os.getenv("FAST_API_PORT")
    try:
        port = int(FAST_API_PORT)
    except ValueError:
        logger.critical("FAST_API_PORT environment variable is not set or is not int")
        sys.exit(1)
    else:
        logger.info("Starting uvicorn server")
        uvicorn.run("main:app", host="0.0.0.0", port=port)
