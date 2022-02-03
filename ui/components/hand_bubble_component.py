
from ui.ui_component import UIComponent


class HandBubbleComponent(UIComponent):

    def __init__(self, x_pos: float, y_pos: float, target: int, color: tuple[int, int, int, int]) -> None:
        super().__init__(x_pos, y_pos)
        self.target: int = target
        self.color: tuple[int, int, int, int] = color