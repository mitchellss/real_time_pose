import sys
import cv2
import numpy as np

from frame_input.frame_input import FrameInput


class VideoFileInput(FrameInput):
    """
    Frame input implementation for a pre-recorded video

    Args:
        FrameInput (): Abstract class for anything that can
        produce a video frame
    """

    def __init__(self, path) -> None:
        self.cap = cv2.VideoCapture(str(path))

    def get_video_frame(self) -> np.ndarray:
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                print("Error getting frame from video file")
                sys.exit(1)


    def close(self):
        # TODO: implement file close method
        print("UNIMPLEMENTED")
        pass

    