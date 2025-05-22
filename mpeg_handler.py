from video import Video
import subprocess

class VideoHandler:
    def __init__(self, video: Video, start_command: tuple = ('',), execute_path: str = "A:\\code\\video-handler\\"):
        self.videos = video
        self._execute_path = execute_path
        self.process = subprocess.Popen(["cd", f"{execute_path}", *start_command], stdout=subprocess.PIPE, cwd='ffmpeg/bin/')

class FFmpegHandler(VideoHandler):
    def __init__(self, video:Video):
        super().__init__(video, ("FFmpeg", "-i", "test_input.mp4", "test_output.mp4"))

class FFprobeHandler:
    def __init__(self, video:Video):
        super().__init__(video, ("FFprobe", "-i", "test_input.mp4"))

