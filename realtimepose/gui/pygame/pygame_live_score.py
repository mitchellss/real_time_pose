import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from ui.components.live_score_component import LiveScoreComponent
import pygame


class PyGameLiveScore(LiveScoreComponent):

    def __init__(self, x_pos: float, y_pos: float, **kwargs) -> None:
        super().__init__(x_pos, y_pos, **kwargs)
        self.words = pygame.font.SysFont(self.font, self.size)

    def draw(self, surface) -> None:
        img = self.words.render(self.text, True, (255,255,255))
        surface.blit(img, (self.x_pos, self.y_pos))

    def set_score(self, score: int) -> None:
        super().set_score(score)
        self.text = f"Score: {round(self.score,1)}"
    
    def add_score(self, score: int) -> None:
        super().add_score(score)
        self.text = f"Score: {round(self.score,1)}"
