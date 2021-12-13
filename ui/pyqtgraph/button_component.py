
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from ui.pyqtgraph.component import Component

class ButtonComponent(Component):

    def __init__(self, size: int, brush: QtGui.QBrush, x_pos: float, y_pos: float, **kwargs) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.button = pg.ScatterPlotItem(size=size, brush=brush)
        self.button.setData(pos=[[x_pos,y_pos]])

        self.func = lambda : True
        if "func" in kwargs:
            self.func = kwargs["func"]
        
        if "target_pts" in kwargs:
            self.target_pts = kwargs["target_pts"]
        else:
            self.target_pts = [0]

    def get_item(self):
        return self.button

    def set_pos(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.button.setData(pos=[[x_pos,y_pos]])

    def is_clicked(self, x, y, distance) -> bool:
        dist = abs((self.x_pos - x)**2 + (self.y_pos - y)**2)**0.5
        if dist < distance:
            self.func()
            return True
        else:
            return False
