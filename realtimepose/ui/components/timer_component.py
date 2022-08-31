from ..ui_component import UIComponent


class TimerComponent(UIComponent):

    def __init__(self, x_pos: float, y_pos: float, **kwargs) -> None:
        super().__init__(x_pos, y_pos)
        self.active: bool = False
        self.time: float = 0

        if "func" in kwargs:
            self.func = kwargs["func"]
        else:
            self.func = lambda: True

        if "size" in kwargs:
            self.size = kwargs["size"]
        else:
            self.size = 30
        
        if "font" in kwargs:
            self.font = kwargs["font"]
        else:
            self.font = "Arial"

    
    def set_pos(self, x_pos: float, y_pos: float) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
    
    def set_timer(self, time: float) -> None:
        self.time = time

    def get_time(self) -> float:
        return self.time
    
    def tick(self) -> None:
        pass

    def start_timer(self) -> None:
        self.active = True

    def stop_timer(self) -> None:
        self.active = False

    def time_expire(self) -> None:
        self.func()