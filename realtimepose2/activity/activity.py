"""Test"""
from typing import List

from realtimepose2.core.displaying.components import Component

from .scene import Scene
from ..core.displaying import UserInterface
from ..core.recieving import PoseGenerator


class Activity:
    """Test"""

    scenes: List[Scene] = []
    active_components: List[Component] = []

    def __init__(self, pose_input: PoseGenerator, frontend: UserInterface) -> None:
        self.pose_input = pose_input
        self.frontend = frontend

    def add_scene(self, scene: Scene):
        """Test"""
        self.scenes.append(scene)

    def run(self):
        """Test"""
        self.frontend.new_gui()
        while True:
            self.frontend.update()
