import numpy as np

class FrameInput():
    """
    Interface for defining an abstract frame input
    device that is capable of sending ndarrays when
    called upon.
    """
    
    def __init__(self) -> None:
        self.has_depth = False

    def get_frame(self) -> np.ndarray:
        """Returns an np.ndarray representing a single frame"""
        pass
    
    def get_depth_frame(self) -> np.ndarray:
        """Returns an np.ndarray representing a single depth frame"""
        pass

    def get_frame_width(self) -> int:
        """Returns the frame width of the frames being sent"""
        pass

    def get_frame_height(self) -> int:
        """Returns the frame height of the frames being sent"""
        pass