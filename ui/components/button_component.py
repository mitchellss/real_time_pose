from ui.ui_component import UIComponent


class ButtonComponent(UIComponent):

    def __init__(self, size: int, color: tuple[int, int, int, int], x_pos: float,
                 y_pos: float, precision: float = 0, **kwargs) -> None:
        self.size: int = size
        self.color: tuple[int, int, int, int] = color
        self.x_pos: float = x_pos
        self.y_pos: float = y_pos
        self.precision: float = precision

    def is_clicked(self, x: float, y: float, distance: float) -> bool:
        pass

    def change_color(self, color: tuple[int, int, int, int]):
        pass
