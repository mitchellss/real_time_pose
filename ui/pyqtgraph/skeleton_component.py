
from ui.component import Component
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.functions import mkBrush, mkColor
import numpy as np

class SkeletonComponent(Component):

    # Where to connect limbs. Refer to here 
    # https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png
    CONNECTIONS = np.array([
        [16,14], [16,18], [16,20], [16,22],
        [18,20], [14,12], [12,11], [12,24],
        [11,23], [11,13], [15,13], [15,17],
        [15,19], [15,21], [17,19], [24,23],
        [26,24], [26,28], [25,23], [25,27],
        [10,9], [8,6], [5,6], [5,4], [0,4],
        [0,1], [2,1], [2,3], [3,7], [28,32],
        [28,30], [27,29], [27,31], [32,30],
        [29,31]
    ])

    RIGHT_HAND = 15
    LEFT_HAND = 16

    def __init__(self, skeleton_array) -> None:
        self.skeleton = pg.GraphItem()
        self.skeleton_array = skeleton_array
        self.skeleton.setData(pos=self.skeleton_array, 
                                adj=self.CONNECTIONS, 
                                pen=pg.mkPen(mkColor(255,255,255,120),width=2),
                                symbolBrush=mkBrush(255,255,255,120),
                                symbolPen=None)

    def get_item(self):
        return self.skeleton

    def set_pos(self, skeleton_array):
        self.skeleton.setData(pos=skeleton_array)
