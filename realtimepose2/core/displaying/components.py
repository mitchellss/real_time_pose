
"""test"""
from typing import Any, Callable
from typing_extensions import Protocol


class Component(Protocol):
    """test"""
    x_coord: float
    y_coord: float

    def render(self, window: Any):
        """test"""


class Button(Protocol):
    """teset"""
    x_coord: float
    y_coord: float

    def is_clicked(self, x_coord: float, y_coord: float, distance: float) -> bool:  # type: ignore
        """test"""

    def render(self, window: Any):
        """test"""


class HasButton(Protocol):
    """test"""

    def button(self, x_coord: float, y_coord: float) -> Button:  # type: ignore
        """test"""


def button(gui: HasButton, x_coord: float, y_coord: float) -> Button:
    """test"""
    return gui.button(x_coord=x_coord, y_coord=y_coord)
