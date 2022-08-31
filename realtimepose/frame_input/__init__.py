
from .frame_input import FrameInput
from .realsense import Realsense
from .video_file_input import VideoFileInput
from .webcam import Webcam

VIDEO_FILE = 0
REALSENSE = 1
WEBCAM = 2

def new_input(type: int, fps: int) -> FrameInput:
    if type == VIDEO_FILE:
        return VideoFileInput()
    elif type == REALSENSE:
        return Realsense()
    elif type == WEBCAM:
        return Webcam()
