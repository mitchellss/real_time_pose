"""Test"""
import sys
import pygame
from pygame.constants import QUIT
from realtimepose2.core.displaying.components import Button

WINDOW_WIDTH: int = 1920//2
WINDOW_HEIGHT: int = 1000


class PyGameUI:
    """test"""
    FPS = 60
    BACKGROUND = (0, 0, 0)

    window: pygame.surface.Surface
    fps_clock: pygame.time.Clock

    def add_component(self, component):
        """test"""

    def clear(self):
        """test"""

    def update(self):
        """test"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

    def button(self, x_coord: float, y_coord: float) -> Button:
        """tset"""
        return PyGameButton(x_coord=x_coord, y_coord=y_coord)

    def new_gui(self):
        """test"""
        pygame.init()
        pygame.font.init()

        # pygame_icon = pygame.image.load('ui/pygame/forsyth-jason.jpg')
        # pygame.display.set_icon(pygame_icon)
        # Colours

        # Game Setup
        self.fps_clock = pygame.time.Clock()

        self.window: pygame.surface.Surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
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

    def render(self):
        """test"""
        print("pygame render")
