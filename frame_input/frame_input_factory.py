

from typing import Tuple
from frame_input.frame_input import FrameInput
from frame_input.realsense import Realsense
from frame_input.video_file_input import VideoFileInput
from frame_input.webcam import Webcam


class FrameInputFactory():
    
    def __init__(self, path) -> None:
        self.path = path
    
    def get_frame_input(self, frame_input_name: str) -> Tuple[FrameInput, int]:
        # Select video input method
        if frame_input_name == "file":
            return(VideoFileInput(self.path), 30)
        if frame_input_name == "webcam":
            return(Webcam(), 20)
        if frame_input_name == "realsense":
            return(Realsense(), 30)
