import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from ui.components.text_component import TextComponent
import pygame
# from ui.pygame.pygame_constants import FONT


class PyGameText(TextComponent):

    def __init__(self, x_pos: float, y_pos: float, text: str, **kwargs) -> None:
        super().__init__(x_pos, y_pos, text, **kwargs)
        self.font = pygame.font.SysFont(self.font, self.size)

    def draw(self, surface: pygame.Surface) -> None:
        img = self.font.render(self.text, True, self.color)
        surface.blit(img, (self.x_pos, self.y_pos))