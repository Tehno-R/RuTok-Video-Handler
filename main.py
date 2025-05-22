from typing import Union
from fastapi import FastAPI

from video import Video
from mpeg_handler import FFmpegHandler, FFprobeHandler

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    vid1 = Video("vid1", "for_testing/test_input.mp4")
    handler1 = FFmpegHandler(vid1)
    handler2 = FFprobeHandler(vid1)