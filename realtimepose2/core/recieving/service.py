from typing import Any
from typing_extensions import Protocol


class CVModel(Protocol):
    def get_pose(self, frame):
        """"""

class FrameInput(Protocol):
    def get_frame(self):
        """"""

class PoseGenerator(Protocol):
    def get_pose(self):
        """"""