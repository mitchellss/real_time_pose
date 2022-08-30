
from realtimepose.frame_input.realsense import Realsense
from realtimepose.frame_input.video_file_input import VideoFileInput
from realtimepose.frame_input.webcam import Webcam

VIDEO_FILE = 0
REALSENSE = 1
WEBCAM = 2

def new_input(type: int, fps: int) -> FrameInput:
    if type == FILE_INPUT:
        return VideoFileInput()
    elif type == REALSENSE:
        return Realsense()
    elif type == WEBCAM:
        return Webcam()
