
import pygame
from ui.components.hand_bubble_component import HandBubbleComponent


class PyGameHandBubble(HandBubbleComponent):

    def __init__(self, x_pos: float, y_pos: float, target: int, color: tuple[int, int, int, int]) -> None:
        super().__init__(x_pos, y_pos, target, color)

    def draw(self, surface) -> None:
        pygame.draw.circle(surface, self.color, (self.x_pos*300+300, self.y_pos*300+300), 20)
    
