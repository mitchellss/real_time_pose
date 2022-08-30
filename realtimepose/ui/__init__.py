
from realtimepose.ui.pygame.pygame_ui import PyGameUI


PYGAME = 0
PYQTGRAPH = 1

def new_gui(frontend=int) -> GUI:
    if frontend == PYGAME:
        return PyGameUI()
    elif frontend == PYQTGRAPH:
        return PyQtGraph()