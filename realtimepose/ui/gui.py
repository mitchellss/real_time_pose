
class GUI():
    """
    Abstract representation of a graphical user interface
    capable of having components added to it
    """
    def __init__(self) -> None:
        self.window = None

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