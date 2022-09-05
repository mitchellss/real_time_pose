
"""test"""
from typing import Any, Callable
from typing_extensions import Protocol, runtime_checkable
import numpy as np


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


@runtime_checkable
class Skeleton(Protocol):
    """test"""
    x_coord: float
    y_coord: float
    skeleton_points: np.ndarray

    def render(self, window: Any):
        """test"""


class HasSkeleton(Protocol):
    """test"""

    def skeleton(self, x_coord: float, y_coord: float) -> Skeleton:  # type: ignore
        """test"""


def button(gui: HasButton, x_coord: float, y_coord: float) -> Button:
    """test"""
    return gui.button(x_coord=x_coord, y_coord=y_coord)


def skeleton(gui: HasSkeleton, x_coord: float, y_coord: float) -> Skeleton:
    """"""
    return gui.skeleton(x_coord=x_coord, y_coord=y_coord)
