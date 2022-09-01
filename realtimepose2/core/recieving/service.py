"""Test"""
from typing_extensions import Protocol
import numpy as np


class CVModel(Protocol):
    """Test"""
    def get_pose(self, frame: np.ndarray) -> np.ndarray:  # type: ignore
        """Test"""

class FrameInput(Protocol):
    """Test"""
    def get_frame(self) -> np.ndarray:  # type: ignore
        """Test"""

class PoseGenerator(Protocol):
    """Test"""
    def get_pose(self) -> np.ndarray:  # type: ignore
        """Test"""