class VideoInfo:
    def __init__(self, video_stream: dict):
        self._index = video_stream["index"]
        self._codec_name = video_stream["codec_name"]
        self._width = video_stream["width"]
        self._height = video_stream["height"]
        self._pix_fmt = video_stream["pix_fmt"]

    def get_index(self):
        return self._index
    def get_codec_name(self):
        return self._codec_name
    def get_width(self):
        return self._width
    def get_height(self):
        return self._height
    def get_pix_fmt(self):
        return self._pix_fmt


class AudioInfo:
    def __init__(self, audio_stream: dict):
        self._index = audio_stream["index"]
        self._codec_name = audio_stream["codec_name"]
        self._sample_rate = audio_stream["sample_rate"]
        self._channels = audio_stream["channels"]

    def get_index(self):
        return self._index
    def get_codec_name(self):
        return self._codec_name
    def get_sample_rate(self):
        return self._sample_rate
    def get_channels(self):
        return self._channels


class ProbeInfo:
    def __init__(self, probe: dict):
        self._video_info = VideoInfo(video_stream=probe['streams'][0])
        self._audio_info = AudioInfo(audio_stream=probe['streams'][1])

    def get_video_info(self):
        return self._video_info
    def get_audio_info(self):
        return self._audio_info