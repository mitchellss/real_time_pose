import pyqtgraph as pg
from constants.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from ui.gui import GUI
from PyQt5 import QtCore

class PyQtGraph(GUI):
    """
    PyQtGraph implementation of the abstract GUI interface.
    Takes custom pyqtgraph elements as components.
    """
    def __init__(self, func) -> None:
        super().__init__()
        self.func = func

    def new_gui(self) -> None:
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('2D Game')

        # Create plot and set range
        self.plot = self.win.addPlot()
        self.plot.setXRange(0, WINDOW_WIDTH)
        self.plot.setYRange(0, WINDOW_HEIGHT)
        self.plot.getViewBox().invertY(True)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.func)
        self.timer.start(50)


    def add_component(self, component) -> None:
        self.plot.addItem(component.get_item())
        