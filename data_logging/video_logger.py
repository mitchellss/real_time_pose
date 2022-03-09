
import time
import cv2
from constants.constants import PATH
from data_logging.logger import Logger

class VideoLogger(Logger):


    def __init__(self, fname, frame_width, frame_height) -> None:
        super().__init__(fname)
        path = PATH / "data" / self.folder_name / f"{self.current_time}_{self.fname}.mp4"
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.vid_writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*'DIVX'), 20, (self.frame_width, self.frame_height))

    def log(self, data) -> None:
        if self.logging:
            self.vid_writer.write(data)

    def new_log(self):
        if self.logging:
            self.close()
        self.current_time = int(time.time())
        path = PATH / "data" / self.folder_name / f"{self.current_time}_{self.fname}.mp4"
        self.vid_writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*'DIVX'), 20, (self.frame_width, self.frame_height))

    def close(self):
        self.vid_writer.release()