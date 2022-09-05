"""Test"""
import logging
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
        frame.flags.writeable = False # Shaves about 5ms off each frame by passing by reference, not value
        pose = self.model.get_pose(frame)
        return pose
