"""Test"""
import numpy as np
from realtimepose2.core.recieving.service import CVModel, FrameInput


class ComputerVisionPose:
    """Test"""

    def __init__(self, frame_input: FrameInput, model: CVModel):
        self.frame_input = frame_input
        self.model = model

    def get_pose(self) -> np.ndarray:
        """Test"""
        frame = self.frame_input.get_frame()
        pose = self.model.get_pose(frame)
        return pose
