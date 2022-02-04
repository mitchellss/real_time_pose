from ui.components.hand_bubble_component import HandBubbleComponent
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


class PyQtGraphHandBubble(HandBubbleComponent):

    def __init__(self, x_pos: float, y_pos: float, target: int, size: int, color: tuple[int, int, int, int]) -> None:
        super().__init__(x_pos, y_pos, target, size, color)
        self.bubble = pg.ScatterPlotItem(size=size, brush=pg.mkBrush(color[0], color[1], color[2], color[3]))
        self.bubble.setData(pos=[[self.x_pos,self.y_pos]])

    def set_pos(self, x_pos: float, y_pos: float):
        """Sets the position of the bubble on the canvas

        Args:
            x_pos (float): X position to move the button to
            y_pos (float): Y position to move the button to
        """
        super().set_pos(x_pos, y_pos)
        self.bubble.setData(pos=[[x_pos,y_pos]])
    
    def get_item(self):
        return self.bubble

    def hide(self) -> None:
        self.get_item().hide()

    def show(self) -> None:
        self.get_item().show()
    