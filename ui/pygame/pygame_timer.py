
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from ui.components.timer_component import TimerComponent
import pygame


class PyGameTimer(TimerComponent):

    def __init__(self, x_pos: float, y_pos: float, **kwargs) -> None:
        super().__init__(x_pos, y_pos, **kwargs)
        self.font = pygame.font.SysFont(self.font, self.size)
    
    def tick(self) -> None:
        if self.time > 0:
            self.time -= 0.04
        else:
            self.time = 0
            self.time_expire()
            self.stop_timer()

    def draw(self, surface: pygame.Surface) -> None:
        if self.visible:
            img = self.font.render(f"Time: {round(self.time,1)}", True, (255,255,255))
            surface.blit(img, (self.x_pos, self.y_pos))

