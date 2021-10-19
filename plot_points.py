import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

class TwoDimensionGame():

    def __init__(self):
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('2D Game')

        self.initUi()

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.setInterval(1000/50)
        self.timer.start()

    def initUi(self):
        self.body_point_array = np.zeros((33, 2))
        
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('Python Step Counter')
        self.plot = self.win.addPlot()
        self.plot.setXRange(-1, 1)
        self.plot.setYRange(-1, 1)

        self.scatter = pg.ScatterPlotItem(size=10, brush=pg.mkBrush(255, 255, 255, 120)) 
        self.scatter1 = self.plot.addItem(self.scatter)



    def update(self):
        self.x = np.array([1,2,3,4])
        self.y = np.array([1,4,9,16])
        self.scatter.setData(self.x, self.y)



if __name__ == "__main__":
    import sys

    td = TwoDimensionGame()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()