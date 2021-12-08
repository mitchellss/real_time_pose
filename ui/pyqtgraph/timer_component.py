
from ui.component import Component
import pyqtgraph as pg


class TimerComponent(Component):

    def __init__(self, x_pos: float, y_pos: float, **kwargs) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.timer = pg.TextItem(text="Test")
        self.timer.setPos(x_pos, y_pos)
        self.time = 0

        if "font" in kwargs:
            self.timer.setFont(kwargs["font"])
        if "text" in kwargs:
            self.timer.setText(kwargs["text"])
        if "starting_time" in kwargs:
            self.time = kwargs["starting_time"]

    def set_pos(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.timer.SetPos(x_pos, y_pos)

    def hide(self):
        self.timer.hide()

    def get_item(self):
        return self.timer

    def set_timer(self, time: float):
        self.time = time

    def tick(self):
        if self.time > 0:
            self.time -= 0.05
            self.timer.setText(text=f"Time: {round(self.time, 1)}")
        else:
            self.time = 0

    def get_time(self):
        return self.time
