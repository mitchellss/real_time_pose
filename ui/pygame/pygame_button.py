import pygame

from ui.components.button_component import ButtonComponent


class PyGameButton(ButtonComponent):

    def __init__(self, size: int, color: tuple[int, int, int, int], x_pos: float,
                 y_pos: float, precision: float = 0.2, **kwargs) -> None:
        super().__init__(size, color, x_pos, y_pos, precision, **kwargs)
        if "func" in kwargs:
            self.func = kwargs["func"]
        else:
            self.func = lambda: True

        if "target_pts" in kwargs:
            self.target_pts = kwargs["target_pts"]
        else:
            self.target_pts = [0]

    def is_clicked(self, x: float, y: float, distance: float) -> bool:
        if abs(x - self.x_pos) < distance and abs(y - self.y_pos) < distance:
            self.func()
            return True
        else:
            return False

    def change_color(self, color: tuple[int, int, int, int]):
        self.color: tuple[int, int, int, int] = color

    def set_pos(self, x_pos: float, y_pos: float) -> None:
        self.x_pos: float = x_pos
        self.y_pos: float = y_pos

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), [100, 100, 400, 100], 0)
