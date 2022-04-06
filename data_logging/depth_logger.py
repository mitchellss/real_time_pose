
import time
import cv2
from constants.constants import PATH
from data_logging.logger import Logger

class DepthLogger(Logger):


    def __init__(self, fname, width, height) -> None:
        super().__init__(fname)
        self.width = width
        self.height = height
        # path = PATH / "data" / self.folder_name / f"{self.current_time}_{self.fname}.mp4"
        # self.frame_width = frame_width
        # self.frame_height = frame_height
        # self.vid_writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*'mp4v'), 30, (self.frame_width, self.frame_height))

    def log(self, depth_frame, landmarks) -> None:
        if landmarks is not None:
            for landmark in range(0,len(landmarks)):
                x = landmarks[landmark].x
                y = landmarks[landmark].y
                relative_x = int(x * self.width)
                relative_y = int(y * self.height)
                if landmark == 15:
                    a = self.get_distance(depth_frame, relative_x, relative_y)
                    print(a, end="\r")
        # if self.logging:
        #     self.vid_writer.write(data)

    # def new_log(self):
    #     if self.logging:
    #         self.close()
    #     self.current_time = int(time.time())
    #     path = PATH / "data" / self.folder_name / f"{self.current_time}_{self.fname}.mp4"
    #     self.vid_writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*'mp4v'), 30, (self.frame_width, self.frame_height))

    # def close(self):
    #     self.vid_writer.release()
    
    
    def get_distance(self, depth_frame, x:int, y:int, flip=True) -> float:
        if flip:
            return depth_frame.get_distance(self._flip(x), y)
        else:
            return depth_frame.get_distance(x,y)
    
    def _flip(self, x: int) -> int:
        return self.width-x
