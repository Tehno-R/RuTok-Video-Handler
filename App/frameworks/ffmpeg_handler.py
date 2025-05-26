from ffmpeg import FFmpeg
import json
import Logger

from domain import Video
from path_controller import PathHandler

logger = Logger.generate_logger("FFmpeg Handler")


class FFmpegHandler:
    _CONTAINER = 'mp4'
    _CODEC_VIDEO = "h264"
    _V_PROFILE = "main"
    _CODEC_AUDIO = "mp3"
    _ASPECT_RATIO = "16:9"
    _RESOLUTION = "1920:1080"
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
        self.to_handle()

    def generate_probe(self) -> dict:
        ffprobe_instance = (
            FFmpeg(executable=PathHandler.get_ffprobe_path().__str__())
            .input(self.input_path.__str__(),
                   print_format="json",
                   show_streams=None)
        )
        return json.loads(ffprobe_instance.execute())

    def to_handle(self):
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
                f=FFmpegHandler._CONTAINER,
                preset="slower"
            )
        )
        ffmpeg_instance.execute()
        logger.info(f"Ending video handle: {self.video.get_uid_name()}")
