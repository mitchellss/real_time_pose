import numpy as np


class PoseDetector():
    """
    Abstract interface representing a pose detection model
    that can return an ndarray of points when given an image.
    """

    def get_pose(self, image: np.ndarray) -> list:
        """Return an np.ndarray of points based on an image."""
        pass