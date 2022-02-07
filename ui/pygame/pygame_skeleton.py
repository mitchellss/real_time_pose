import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from ui.components.skeleton_component import SkeletonComponent


class PyGameSkeleton(SkeletonComponent):

    def __init__(self, skeleton_array):
        super().__init__(skeleton_array)

    def draw(self, surface: pygame.Surface) -> None:
        for i in self.CONNECTIONS:
            pygame.draw.line(surface, (255,255,255), [self.skeleton_array[i[0]][0], self.skeleton_array[i[0]][1]], 
            [self.skeleton_array[i[1]][0], self.skeleton_array[i[1]][1]], 2)
            
        for i in range(0, len(self.skeleton_array)):
            pygame.draw.circle(surface, (0, 255, 0), [self.skeleton_array[i][0],self.skeleton_array[i][1]], 5, 0)
            

    def set_pos(self, skeleton_array):
        self.skeleton_array = skeleton_array
