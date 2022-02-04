
import pyqtgraph as pg
from ui.components.timer_component import TimerComponent


class PyQtGraphTimer(TimerComponent):

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

        if "func" in kwargs:
            self.func = kwargs["func"]
        else:
            self.func = lambda : True

    def set_pos(self, x_pos: float, y_pos: float) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.timer.SetPos(x_pos, y_pos)

    def get_item(self) -> pg.TextItem:
        return self.timer

    def set_timer(self, time: float) -> None:
        self.time = time

    def tick(self) -> None:
        if self.time > 0:
            self.time -= 0.05
            self.timer.setText(text=f"Time: {round(self.time, 1)}")
        else:
            self.time = 0
            self.time_expire()

    def get_time(self) -> float:
        return self.time

    def time_expire(self) -> None:
        self.func()