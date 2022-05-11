import json
import numpy as np

from constants.constants import QUEUE_NAME

class PoseDetection:

    def __init__(self, queue) -> None:
        self.pose: np.ndarray = None


    def get_skeleton(self) -> np.ndarray:
        pass
    