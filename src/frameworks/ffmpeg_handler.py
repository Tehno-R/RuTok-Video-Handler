import json

from ffmpeg import FFmpeg, ffmpeg

import Logger
from path_controller import PathHandler
from video import Video

logger = Logger.generate_logger("FFmpeg Handler")


class FFmpegHandler:
    _VIDEO_FORMAT = 'mp4'
    _IMAGE_FORMAT = 'image2pipe'
    _CODEC_IMAGE = "mjpeg"
    _FRAME_TO_IMAGE = "select=eq(n\,0)"
    _CODEC_VIDEO = "h264"
    _V_PROFILE = "main"
    _CODEC_AUDIO = "mp3"
    _ASPECT_RATIO = "9:16"
    _RESOLUTION = "1080:1920"
    _BITRATE = "27306k"  # kbit/s
    _DURATION = "00:01:00"

    _CODEC_ENCODERS = {
        'h264': "libx264",
        'prores': "prores",
        'mp3': "libmp3lame",
        'aac': "aac",
        'opus': "opus"
    }

    def __init__(self, video: Video):
        self.video = video
        self.input_path = (PathHandler.get_input_path().joinpath(video.get_uid_name()))
        self.output_path = (PathHandler.get_output_path().joinpath(video.get_uid_name()))
        self.ffmpeg_input = FFmpeg().input(self.input_path)
        video.set_probe(self.generate_probe())

    def generate_probe(self) -> dict:
        ffprobe_instance = (
            FFmpeg(executable=PathHandler.get_ffprobe_path().__str__())
            .input(self.input_path.__str__(),
                   print_format="json",
                   show_streams=None)
        )
        return json.loads(ffprobe_instance.execute())

    def to_handle(self) -> int:
        logger.info(f"Starting video handle: {self.video.get_uid_name()}")

        video_encoder = self._CODEC_ENCODERS[self._CODEC_VIDEO]
        audio_encoder = self._CODEC_ENCODERS[self._CODEC_AUDIO]

        ffmpeg_instance = (
            FFmpeg(executable=PathHandler.get_ffmpeg_path().__str__())
            # .option("y")
            .input(self.input_path)
            .output(
                self.output_path,
                {"codec:v": video_encoder,
                 "profile:v": self._V_PROFILE,
                 "codec:a": audio_encoder},
                vf=f"scale={self._RESOLUTION}",
                to=self._DURATION,
                pix_fmt="yuv420p",
                aspect=self._ASPECT_RATIO,
                maxrate=self._BITRATE,
                f=FFmpegHandler._VIDEO_FORMAT,
                preset="fast"
            )
        )
        try:
            ffmpeg_instance.execute()
        except ffmpeg.FFmpegError:
            logger.error(f"Error handle video file: {self.video.get_uid_name()}")
            return 1
        logger.info(f"Video handle successful: {self.video.get_uid_name()}")

        ffmpeg_instance = (
            FFmpeg(executable=PathHandler.get_ffmpeg_path().__str__())
            # .option("y")
            .input(self.output_path)
            .output(
                self.output_path.__str__() + "_preview",
                {"c:v": self._CODEC_IMAGE,
                        "vf": "select=eq(n\\,0)"},
                vframes=1,
                f=FFmpegHandler._IMAGE_FORMAT
            )
        )
        try:
            ffmpeg_instance.execute()
        except ffmpeg.FFmpegError:
            logger.error(f"Error handle preview file: {self.video.get_uid_name()}")
            return 1
        logger.info(f"Preview handle successful: {self.video.get_uid_name()}")

        logger.info(f"Ending video handle: {self.video.get_uid_name()}")
        return 0
