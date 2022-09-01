
from typing_extensions import Protocol


class UserInterface(Protocol):

    def add_component(self, component) -> None:
        """"""

    def clear(self) -> None:
        """"""