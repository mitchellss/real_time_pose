
import pygame
from ui.gui import GUI
from ui.pygame.pygame_component import PyGameComponent


class PyGameUI(GUI):

    def new_gui(self) -> None:
        pygame.init()
        # Colours
        BACKGROUND = (255, 255, 255)
        
        # Game Setup
        FPS = 60
        fpsClock = pygame.time.Clock()
        WINDOW_WIDTH = 400
        WINDOW_HEIGHT = 300
        
        self.window: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('My Game!')


    def add_component(self, component: PyGameComponent) -> None:
        component.draw_component(self.window)