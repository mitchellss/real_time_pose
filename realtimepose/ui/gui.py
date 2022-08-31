
from typing_extensions import Protocol


class GUI(Protocol):
    """
    Abstract representation of a graphical user interface
    capable of having components added to it
    """
    def new_gui(self) -> None:
        pass

    def add_component(self, component) -> None:
        pass

    def update(self) -> None:
        pass

    def clear(self) -> None:
        pass

    def quit(self) -> None:
        pass