from ui.ui_component import UIComponent


class ButtonComponent(UIComponent):

    def __init__(self, size: int, color: tuple[int, int, int, int], x_pos: float,
                 y_pos: float, precision: float = 0, **kwargs) -> None:
        self.size: int = size
        self.color: tuple[int, int, int, int] = color
        self.x_pos: float = x_pos
        self.y_pos: float = y_pos
        self.precision: float = precision
        self.clicked: bool = False
        if "func" in kwargs:
            self.func = kwargs["func"]
        else:
            self.func = lambda: True

        if "target_pts" in kwargs:
            self.target_pts = kwargs["target_pts"]
        else:
            self.target_pts = [0]

    def is_clicked(self, x: float, y: float, distance: float) -> bool:
        pass

    def change_color(self, color: tuple[int, int, int, int]):
        pass
