
class UIComponent:

    def __init__(self, x_pos: float, y_pos: float) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos

    def set_pos(self, x_pos: float, y_pos: float) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos

    def hide(self) -> None:
        pass

    def show(self) -> None:
        pass

    def draw(self, surface) -> None:
        pass
