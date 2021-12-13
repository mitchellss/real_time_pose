
import cv2
from constants.constants import PATH
from data_logging.logger import Logger
import pathlib

class VideoLogger(Logger):


    def __init__(self, fname, **kwargs) -> None:
        super().__init__(fname)
        path = PATH / "data" / fname / f"{fname}.mp4"
        self.vid_writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*'DIVX'), 20, (kwargs["frame_width"], kwargs["frame_height"]))

    def log(self, data):
        self.vid_writer.write(data)

    def close(self):
        self.vid_writer.release()