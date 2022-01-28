
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from ui.pyqtgraph.component import Component

class ButtonComponent(Component):
    """
    PyQtGraph implementation of a button. Can be programmed to do abstract tasks
    when clicked.

    Args:
        Component ([type]): Abstract component
    """

    def __init__(self, size: int, brush: QtGui.QBrush, x_pos: float, y_pos: float, precision: float = 0.2, **kwargs) -> None:
        """Initializes a button

        Args:
            size (int): Size of the button to be created
            brush (QtGui.QBrush): Brush used to draw the button
            x_pos (float): Starting X position of the button
            y_pos (float): Starting Y postiion of the button
            precision (float, optional): How close the user needs to get to the button to actuate. Defaults to 0.2.
        """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.button = pg.ScatterPlotItem(size=size, brush=brush)
        self.button.setData(pos=[[x_pos,y_pos]])
        self.precision: float = precision
        self.clicked: bool = False

        self.func = lambda : True
        if "func" in kwargs:
            self.func = kwargs["func"]
        
        if "target_pts" in kwargs:
            self.target_pts = kwargs["target_pts"]
        else:
            self.target_pts = [0]

    def get_item(self):
        return self.button

    def set_pos(self, x_pos: float, y_pos: float):
        """Sets the position of the button on the canvas

        Args:
            x_pos (float): X position to move the button to
            y_pos (float): Y position to move the button to
        """
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.button.setData(pos=[[x_pos,y_pos]])

    def is_clicked(self, x: float, y: float, distance: float) -> bool:
        """Checks to see if the button is clicked and returns True if so

        Args:
            x (float): X position of point relative to button
            y (float): Y position of point relative to button
            distance (float): How close the relative point needs to be for actuation

        Returns:
            bool: If the button is considered clicked or not
        """
        dist = abs((self.x_pos - x)**2 + (self.y_pos - y)**2)**0.5
        if dist < distance:
            self.func() # Executes button function
            return True
        else:
            return False
