import sys

import pygame
from pygame.constants import QUIT

from ui.gui import GUI
from ui.ui_component import UIComponent


class PyGameUI(GUI):

    FPS = 60
    BACKGROUND = (255, 255, 255)

    def new_gui(self) -> None:
        pygame.init()
        # Colours

        # Game Setup
        self.fpsClock = pygame.time.Clock()
        WINDOW_WIDTH = 1000
        WINDOW_HEIGHT = 600
        
        self.window: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('My Game!')
        self.window.fill(self.BACKGROUND)


    def add_component(self, component: UIComponent) -> None:
        component.draw(self.window)

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # Processing
            # This section will be built out later
        
            # Render elements of the game
            self.window.fill(self.BACKGROUND)
            pygame.draw.rect(self.window, (255,0,0), [100,100,400,100], 0)
            pygame.display.update()
            self.fpsClock.tick(self.FPS)
