"""Test"""
from realtimepose.core.displaying.components import Button


class Pyglet:
    """Test"""

    def add_component(self, component):
        """Test"""

    def clear(self):
        """Test"""

    def button(self, x_coord: float, y_coord: float) -> Button:
        """Test"""
        return PygletButton(x_coord, y_coord)


class PygletButton:
    """Test"""
    def __init__(self, x_coord: float, y_coord: float) -> None:
        self.x_coord = x_coord
        self.y_coord = y_coord

    def is_clicked(self, x_coord: float, y_coord: float, distance: float) -> bool:
        """Test"""
        return False

    def render(self):
        """Test"""
        print("pyglet render")
