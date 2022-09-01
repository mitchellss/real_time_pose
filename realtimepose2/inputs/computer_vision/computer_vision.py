from realtimepose2.core.recieving.service import CVModel, FrameInput
import numpy as np

class ComputerVisionPose:
    """"""
    def __init__(self, frame_input: FrameInput, model: CVModel):
        self.frame_input = frame_input
        self.model = model

    def get_pose(self) -> np.array:
        """"""
        frame = self.frame_input.get_frame()
        pose = self.model.get_pose(frame)
        return pose