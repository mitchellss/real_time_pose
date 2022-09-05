
from typing_extensions import Protocol


class UIComponent(Protocol):

    # def __init__(self, x_pos: float, y_pos: float) -> None:
    #     self.x_pos = x_pos
    #     self.y_pos = y_pos
    #     self.visible = True

    def set_pos(self, x_pos: float, y_pos: float) -> None:
        pass
        # self.x_pos = x_pos
        # self.y_pos = y_pos

    def hide(self) -> None:
        pass
        # self.visible = False

    def show(self) -> None:
        pass
        # self.visible = True

    def draw(self, surface) -> None:
        pass
