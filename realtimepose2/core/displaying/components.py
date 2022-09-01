
"""test"""
from typing_extensions import Protocol


class Component(Protocol):
    """test"""
    x_coord: float
    y_coord: float

    def render(self):
        """test"""


class Button(Protocol):
    """teset"""
    x_coord: float
    y_coord: float

    def is_clicked(self, x_coord: float, y_coord: float, distance: float) -> bool:  # type: ignore
        """test"""

    def render(self):
        """test"""


class HasButton(Protocol):
    """test"""

    def button(self, x_coord: float, y_coord: float) -> Button:  # type: ignore
        """test"""


def button(gui: HasButton, x_coord: float, y_coord: float) -> Button:
    """test"""
    return ButtonImpl(gui, x_coord, y_coord)


class ButtonImpl:
    """test"""

    def __init__(self, gui: HasButton, x_coord: float, y_coord: float) -> None:
        self.gui = gui
        self.x_coord = x_coord
        self.y_coord = y_coord

    def is_clicked(self, x_coord: float, y_coord: float, distance: float) -> bool:
        """test"""
        if abs(self.x_coord - x_coord) < distance and abs(self.y_coord - y_coord) < distance:
            return True
        return False

    def render(self):
        """test"""
        print("Shared render logic")
        self.gui.button(self.x_coord, self.y_coord).render()
