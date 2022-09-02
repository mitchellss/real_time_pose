"""Test"""
import sys
from typing import Callable
import pygame
from pygame.constants import QUIT
from realtimepose2.core.displaying.components import Button, Skeleton
import numpy as np


class PyGameUI:
    """test"""
    BACKGROUND = (0, 0, 0)

    window: pygame.surface.Surface
    fps_clock: pygame.time.Clock

    def __init__(self, height: int, width: int, fps: int) -> None:
        self.width = width
        self.height = height
        self.fps = fps

    def clear(self):
        """test"""

    def update(self):
        """test"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        self.fps_clock.tick(self.fps)

    def button(self, x_coord: float, y_coord: float) -> Button:
        """tset"""
        return PyGameButton(x_coord=x_coord, y_coord=y_coord)

    def skeleton(self, x_coord: float, y_coord: float) -> Skeleton:
        """test"""
        return PyGameSkeleton(x_coord=x_coord, y_coord=y_coord)

    def new_gui(self):
        """test"""
        pygame.init()
        pygame.font.init()

        # Game Setup
        self.fps_clock = pygame.time.Clock()

        self.window: pygame.surface.Surface = pygame.display.set_mode(
            (self.width, self.height))
        pygame.display.set_caption('WCRG Video Feedback System')
        self.window.fill(self.BACKGROUND)


class PyGameButton:
    """test"""

    def __init__(self, x_coord: float, y_coord: float) -> None:
        """test"""
        self.x_coord = x_coord
        self.y_coord = y_coord

    def is_clicked(self, x_coord: float, y_coord: float, distance: float) -> bool:
        """test"""
        return False

    def render(self, window):
        """test"""
        pygame.draw.circle(
            window, pygame.color.Color(255, 0, 0, 255),
            (self.x_coord, self.y_coord),
            100
        )


class PyGameSkeleton:
    """"""

    # Where to connect limbs. Refer to here
    # https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png
    CONNECTIONS = np.array([
        [16, 14], [16, 18], [16, 20], [16, 22],
        [18, 20], [14, 12], [12, 11], [12, 24],
        [11, 23], [11, 13], [15, 13], [15, 17],
        [15, 19], [15, 21], [17, 19], [24, 23],
        [26, 24], [26, 28], [25, 23], [25, 27],
        [10, 9], [8, 6], [5, 6], [5, 4], [0, 4],
        [0, 1], [2, 1], [2, 3], [3, 7], [28, 32],
        [28, 30], [27, 29], [27, 31], [32, 30],
        [29, 31]
    ])

    def __init__(self, x_coord: float, y_coord: float) -> None:
        """test"""
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.skeleton_points = np.zeros((33, 4))

    def render(self, window):
        """test"""
        for i in self.CONNECTIONS:
            pygame.draw.line(window, (255, 255, 255), [self.skeleton_points[i[0]][0], self.skeleton_points[i[0]][1]],
                             [self.skeleton_points[i[1]][0], self.skeleton_points[i[1]][1]], 2)

        for i in range(0, len(self.skeleton_points)):
            pygame.draw.circle(window, (0, 255, 0), [
                               self.skeleton_points[i][0], self.skeleton_points[i][1]], 5, 0)
