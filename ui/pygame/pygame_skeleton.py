import pygame

from ui.components.skeleton_component import SkeletonComponent


class PyGameSkeleton(SkeletonComponent):

    def __init__(self, skeleton_array) -> None:
        self.skeleton_array = skeleton_array

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (255, 0, 0), [100, 100, 400, 100], 0)

    def set_pos(self, skeleton_array):
        self.skeleton_array = skeleton_array
