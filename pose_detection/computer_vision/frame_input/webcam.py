import numpy as np
import cv2

from pose_detection.computer_vision.frame_input.frame_input import FrameInput

class Webcam(FrameInput):
    """FrameInput implementation representing a video capture 0 webcam"""

    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(0)
        self.vid_width= int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.vid_height= int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_frame(self) -> np.ndarray:
        success, color_image = self.cap.read()
        if not success:
            return None
        return color_image
    
    def get_frame_width(self) -> int:
        return int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    def get_frame_height(self) -> int:
        return int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))