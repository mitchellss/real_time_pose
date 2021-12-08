import pyqtgraph as pg
from ui.gui import GUI


class PyQtGraph(GUI):

    def new_gui(self) -> None:
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('2D Game')

        # Create plot and set range
        self.plot = self.win.addPlot()
        self.plot.setXRange(-1, 1)
        self.plot.setYRange(-1.2, 0.8)
        self.plot.getViewBox().invertY(True)

    def add_component(self, component) -> None:
        self.plot.addItem(component.get_item())
        