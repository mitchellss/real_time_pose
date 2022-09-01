from typing import Any
from typing_extensions import Protocol


class CVModel(Protocol):
    def get_pose(self, frame: np.array) -> np.array:
        """"""

class FrameInput(Protocol):
    def get_frame(self) -> np.array:
        """"""

class PoseGenerator(Protocol):
    def get_pose(self) -> np.array:
        """"""