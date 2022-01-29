
class Component():
    """
    Abstract representation of a PyQtGraph component, exposing only necessary methods
    """

    def set_pos(self, x_pos, y_pos) -> None:
        pass

    def hide(self) -> None:
        self.get_item().hide()

    def show(self) -> None:
        self.get_item().show()

    def get_item(self):
        pass