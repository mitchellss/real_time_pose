"""Test"""
from typing_extensions import Protocol

from realtimepose2.core.displaying.components import Button


class UserInterface(Protocol):
    """Test"""

    def clear(self) -> None:
        """Test"""

    def new_gui(self) -> None:
        """Test"""

    def button(self, x_coord: float, y_coord: float) -> Button:  # type: ignore
        """Test"""

    def update(self):
        """Test"""
