from ui.ui_component import UIComponent
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


class PyQtGraphHandBubble(UIComponent):

    def __init__(self, size: int, brush: QtGui.QBrush, x_pos: float, y_pos: float, target: int, **kwargs) -> None:
        self.bubble = pg.ScatterPlotItem(size=size, brush=brush)
        self.bubble.setData(pos=[[x_pos,y_pos]])
        self.target: int = target

    def set_pos(self, x_pos: float, y_pos: float):
        """Sets the position of the bubble on the canvas

        Args:
            x_pos (float): X position to move the button to
            y_pos (float): Y position to move the button to
        """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.bubble.setData(pos=[[x_pos,y_pos]])
    
    def get_item(self):
        return self.bubble

    def hide(self) -> None:
        self.get_item().hide()

    def show(self) -> None:
        self.get_item().show()
    