from typing_extensions import Protocol
import numpy as np


class CVModel(Protocol):
    """
    Abstract interface representing a pose detection model
    that can return an ndarray of points when given an image.
    """
    NUM_LANDMARKS = 33

    def __init__(self) -> None:
        # Array of the 33 mapped points
        self.skeleton_array = np.zeros((self.NUM_LANDMARKS, 4))

    def get_pose(self, image: np.ndarray) -> np.ndarray:
        """Return an np.ndarray of points based on an image."""
        pass