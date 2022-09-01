from typing import List

from .scene import Scene
from ..core.displaying import UserInterface
from ..core.recieving import PoseGenerator

class Activity:
    """"""

    scenes: List[Scene] = []

    def __init__(self, input: PoseGenerator, frontend: UserInterface) -> None:
        """"""

    def add_scene(self, scene: Scene):
        self.scenes.append(scene)
    
    def run(self):
        """"""