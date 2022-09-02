from typing_extensions import Protocol
import numpy as np


class FrameInput(Protocol):
    """
    Interface for defining an abstract frame input
    device that is capable of sending ndarrays when
    called upon.
    """

    def get_video_frame(self) -> np.ndarray:  # type: ignore
        """Returns an np.ndarray representing a single frame"""

    def get_frame_width(self) -> int:  # type: ignore
        """Returns the frame width of the frames being sent"""

    def get_frame_height(self) -> int:  # type: ignore
        """Returns the frame height of the frames being sent"""

    def close(self):
        """Closes the source of the frame input"""
