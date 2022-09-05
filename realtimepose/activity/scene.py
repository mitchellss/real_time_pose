"""Test"""
from typing import List
from realtimepose.core.displaying.components import Component


class Scene:
    """Test"""

    def __init__(self) -> None:
        self.components: List[Component] = []

    def add_component(self, component: Component):
        """Test"""
        self.components.append(component)
