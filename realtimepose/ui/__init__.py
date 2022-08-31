
from .gui import GUI
from .pygame.pygame_ui import PyGameUI


PYGAME = 0

def new_gui(frontend=int) -> GUI:
    if frontend == PYGAME:
        return PyGameUI()