
import pyqtgraph as pg
from pyqtgraph.functions import mkBrush, mkColor
from ui.components.skeleton_component import SkeletonComponent


class PyQtGraphSkeleton(SkeletonComponent):

    RIGHT_HAND = 15
    LEFT_HAND = 16

    def __init__(self, skeleton_array) -> None:
        super().__init__(skeleton_array)
        self.skeleton = pg.GraphItem()
        self.skeleton.setData(pos=self.skeleton_array, 
                                adj=self.CONNECTIONS, 
                                pen=pg.mkPen(mkColor(255,255,255,120),width=2),
                                symbolBrush=mkBrush(255,255,255,120),
                                symbolPen=None)

    def get_item(self):
        return self.skeleton

    def set_pos(self, skeleton_array):
        self.skeleton.setData(pos=skeleton_array)

    def hide(self) -> None:
        self.get_item().hide()

    def show(self) -> None:
        self.get_item().show()
