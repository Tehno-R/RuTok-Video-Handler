import os
import shutil
import sys
import Logger
from os import mkdir
from pathlib import Path
import dotenv

from domain import Video

logger = Logger.generate_logger("Path Controller")


class PathHandler:
    _WORK_DIRECTORY_PATH = Path(__file__).resolve().parent.parent.parent
    _INPUT_PATH = None
    _OUTPUT_PATH = None
    _FFMPEG_BINARY_PATH = None
    _FFPROBE_BINARY_PATH = None
    _ready_to_work = False

    def __init__(self):
        raise TypeError("Нельзя создавать экземпляры статического класса")

    @staticmethod
    def load_env_variables():
        dotenv.load_dotenv(PathHandler._WORK_DIRECTORY_PATH.joinpath(".env"))

    @staticmethod
    def refresh_paths(refresh_directories: bool = True):
        PathHandler._INPUT_PATH = PathHandler._WORK_DIRECTORY_PATH.joinpath(Path(os.getenv("INPUT_PATH")))
        PathHandler._OUTPUT_PATH = PathHandler._WORK_DIRECTORY_PATH.joinpath(Path(os.getenv("OUTPUT_PATH")))
        PathHandler._FFMPEG_BINARY_PATH = PathHandler._WORK_DIRECTORY_PATH.joinpath(Path(os.getenv("FFMPEG_BINARY_PATH")))
        PathHandler._FFPROBE_BINARY_PATH = PathHandler._WORK_DIRECTORY_PATH.joinpath(Path(os.getenv("FFPROBE_BINARY_PATH")))

        if not PathHandler._INPUT_PATH.exists():
            logger.warning("Input path does not exist")
            PathHandler._INPUT_PATH.mkdir()
            logger.info("Input path created")
        if not PathHandler._OUTPUT_PATH.exists():
            logger.warning("Output path does not exist")
            PathHandler._OUTPUT_PATH.mkdir()
            logger.info("Output path created")
        if not PathHandler._FFMPEG_BINARY_PATH.exists():
            logger.critical("FFMPEG_BINARY_PATH not found. Please configure FFMPEG path.")
            sys.exit(1)
        if not PathHandler._FFPROBE_BINARY_PATH.exists():
            logger.critical("FFPROBE_BINARY_PATH not found. Please configure FFPROBE path.")
            sys.exit(1)

        logger.info("Paths refreshed")

        if refresh_directories:
            PathHandler._refresh_directories()
        PathHandler._ready_to_work = True

    @staticmethod
    def check_ready_to_work(func):
        def wrapper(*args, **kwargs):
            if PathHandler._ready_to_work:
                return_value = func(*args, **kwargs)
                return return_value
            else:
                logger.critical("Before, call PathHandler.refresh_paths()")
                sys.exit(1)
        return wrapper

    @staticmethod
    def _refresh_directories():
        shutil.rmtree(PathHandler._INPUT_PATH, onerror=PathHandler._exception_clear_directory_handler)
        mkdir(PathHandler._INPUT_PATH)
        shutil.rmtree(PathHandler._OUTPUT_PATH, onerror=PathHandler._exception_clear_directory_handler)
        mkdir(PathHandler._OUTPUT_PATH)
        logger.info(f"Directories cleaned")

    @staticmethod
    def _exception_clear_directory_handler(function, path, exc_info):
        logger.critical(f"Error cleaning directory: {path}")
        sys.exit(1)

    @staticmethod
    def get_directory_path() -> Path:
        return PathHandler._WORK_DIRECTORY_PATH

    @staticmethod
    @check_ready_to_work
    def get_input_path() -> Path:
        return PathHandler._WORK_DIRECTORY_PATH.joinpath(PathHandler._INPUT_PATH)


    @staticmethod
    @check_ready_to_work
    def get_output_path() -> Path:
        return PathHandler._WORK_DIRECTORY_PATH.joinpath(PathHandler._OUTPUT_PATH)


    @staticmethod
    @check_ready_to_work
    def get_ffmpeg_path() -> Path:
        return PathHandler._FFMPEG_BINARY_PATH

    @staticmethod
    @check_ready_to_work
    def get_ffprobe_path() -> Path:
        return PathHandler._FFPROBE_BINARY_PATH

    @classmethod
    @check_ready_to_work
    def delete_file_from_input(cls, video: Video):
        path_to_delete = PathHandler._INPUT_PATH.joinpath(video.get_uid_name())
        if path_to_delete.exists():
            path_to_delete.unlink()
        else:
            logger.error(f"Can't delete file {PathHandler._INPUT_PATH.joinpath(video.get_uid_name())} from input "
                           f"because it does not exist")

    @classmethod
    @check_ready_to_work
    def delete_file_from_output(cls, video: Video):
        path_to_delete = PathHandler._OUTPUT_PATH.joinpath(video.get_uid_name())
        if path_to_delete.exists():
            path_to_delete.unlink()
        else:
            logger.error(f"Can't delete file {PathHandler._INPUT_PATH.joinpath(video.get_uid_name())} from output "
                           f"because it does not exist")


PathHandler.load_env_variables()
PathHandler.refresh_paths()