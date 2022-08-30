from typing_extensions import Protocol
import numpy as np

class PoseDetection(Protocol):

    def __init__(self) -> None:
        self.pose: np.ndarray = None

    def get_skeleton(self) -> np.ndarray:
        pass
    