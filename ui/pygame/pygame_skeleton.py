
import pygame
from ui.pygame.pygame_component import PyGameComponent


class PyGameSkeleton(PyGameComponent):

    def __init__(self, skeleton_array) -> None:
        self.skeleton_array = skeleton_array

    def draw_component(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (255,0,0), [100,100,400,100], 0)

    def set_pos(self, skeleton_array):
        self.skeleton_array = skeleton_array