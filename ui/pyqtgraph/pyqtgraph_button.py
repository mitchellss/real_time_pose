
import pyqtgraph as pg
from pyqtgraph.functions import mkBrush

from ui.components.button_component import ButtonComponent


class PyQtGraphButton(ButtonComponent):
    """
    PyQtGraph implementation of a button. Can be programmed to do abstract tasks
    when clicked.

    Args:
        Component ([type]): Abstract component
    """

    def __init__(self, size: int, color: tuple[int, int, int, int], x_pos: float, y_pos: float, precision: float = 0.2, **kwargs) -> None:
        """Initializes a button

        Args:
            size (int): Size of the button to be created
            brush (QtGui.QBrush): Brush used to draw the button
            x_pos (float): Starting X position of the button
            y_pos (float): Starting Y position of the button
            precision (float, optional): How close the user needs to get to the button to actuate. Defaults to 0.2.
        """
        super().__init__(size, color, x_pos, y_pos, precision, **kwargs)
        brush = mkBrush(color[0], color[1], color[2], color[3])
        self.button = pg.ScatterPlotItem(size=size, brush=brush)
        self.button.setData(pos=[[x_pos,y_pos]])

        self.func = lambda: True
        if "func" in kwargs:
            self.func = kwargs["func"]
        
        if "target_pts" in kwargs:
            self.target_pts = kwargs["target_pts"]
        else:
            self.target_pts = [0]

    def get_item(self):
        return self.button

    def hide(self) -> None:
        self.get_item().hide()

    def show(self) -> None:
        self.get_item().show()

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

    def change_color(self, color: tuple[int, int, int, int]) -> None:
        self.button.setBrush(mkBrush(color[0], color[1], color[2], color[3]))