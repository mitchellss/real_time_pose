
from ui.components.text_component import TextComponent
import pygame
# from ui.pygame.pygame_constants import FONT


class PyGameText(TextComponent):

    def __init__(self, x_pos: float, y_pos: float, text: str) -> None:
        super().__init__(x_pos, y_pos, text)
        self.font = pygame.font.SysFont("Sans", 30)

    def draw(self, surface: pygame.Surface) -> None:
        img = self.font.render(self.text, True, (255,255,255))
        surface.blit(img, (20,20))