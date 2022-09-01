
from typing_extensions import Protocol

from realtimepose2.core.displaying.components import Button


class UserInterface(Protocol):

    def clear(self) -> None:
        """"""
    
    def button(self, x: float, y: float) -> Button:
        """"""