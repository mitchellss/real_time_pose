"""Test"""
import sys
from typing import Callable, Literal
import pygame
from pygame.constants import QUIT
from realtimepose.core.displaying.components import Button, Skeleton
import numpy as np


class PyGameUI:
    """test"""
    BACKGROUND: tuple[Literal[0], Literal[0], Literal[0]] = (0, 0, 0)

    window: pygame.surface.Surface
    fps_clock: pygame.time.Clock

    def __init__(self, height: int, width: int, fps: int) -> None:
        self.width = width
        self.height = height
        self.fps = fps

    def clear(self) -> None:
        """test"""
        self.window.fill(self.BACKGROUND)

    def update(self) -> None:
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

    def new_gui(self) -> None:
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
        self.x_coord: float = x_coord
        self.y_coord: float = y_coord

    def is_clicked(self, x_coord: float, y_coord: float, distance: float) -> bool:
        """test"""
        return False

    def render(self, window) -> None:
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
    CONNECTIONS: np.ndarray = np.array([
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

    LIMB_COLOR: tuple[Literal[255], Literal[255], Literal[255]] = (255, 255, 255)
    LIMB_WIDTH: Literal[2] = 2

    LANDMARK_COLOR: tuple[Literal[0], Literal[255], Literal[0]] = (0, 255, 0)
    LANDMARK_RADIUS: Literal[5] = 5
    LANDMARK_OUTLINE_WIDTH: Literal[0] = 0

    NUM_LANDMARKS: Literal[33] = 33
    POINTS_PER_LANDMARK: Literal[4] = 4 # x, y, z, depth?

    def __init__(self, x_coord: float, y_coord: float) -> None:
        """test"""
        self.x_coord: float = x_coord
        self.y_coord: float = y_coord
        self.skeleton_points: np.ndarray = np.zeros((33, 4))

    def render(self, window) -> None:
        """test"""
        for landmark_pair in self.CONNECTIONS:
            start_landmark: int = landmark_pair[0]
            end_landmark: int = landmark_pair[1]
            line_start_x: float = self.skeleton_points[start_landmark][0]
            line_start_y: float = self.skeleton_points[start_landmark][1]
            line_end_x: float = self.skeleton_points[end_landmark][0]
            line_end_y: float = self.skeleton_points[end_landmark][1]
            pygame.draw.line(window, self.LIMB_COLOR, [float(line_start_x), float(line_start_y)],
                             [float(line_end_x), float(line_end_y)], self.LIMB_WIDTH)

        for landmark in range(0, len(self.skeleton_points)):
            point_x: float = self.skeleton_points[landmark][0]
            point_y: float = self.skeleton_points[landmark][1]
            pygame.draw.circle(window, self.LANDMARK_COLOR, [point_x, point_y], self.LANDMARK_RADIUS, self.LANDMARK_OUTLINE_WIDTH)
