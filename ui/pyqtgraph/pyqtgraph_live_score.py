import pyqtgraph as pg
from ui.ui_component import UIComponent


class LiveScoreUIComponent(UIComponent):
    """Component used to create a text score counter that can
    be updated in real-time

    Args:
        Component (): Abstract component type
    """
    def __init__(self, x_pos: float, y_pos: float, **kwargs) -> None:
        self.x_pos: float = x_pos
        self.y_pos: float = y_pos
        self.score_count = pg.TextItem(text="Score: ")
        self.score_count.setPos(x_pos, y_pos)
        self.score: int = 0

        if "font" in kwargs:
            self.score_count.setFont(kwargs["font"])
        if "text" in kwargs:
            self.score_count.setText(kwargs["text"])
    
    def set_pos(self, x_pos: float, y_pos: float):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.score_count.SetPos(x_pos, y_pos)

    def get_item(self) -> pg.TextItem:
        return self.score_count

    def set_score(self, score: int) -> None:
        self.score = score
        self.score_count.setText(f"Score: {self.score}")

    def add_score(self, score: int) -> None:
        self.score += score
        self.score_count.setText(f"Score: {self.score}")

    def get_score(self) -> int:
        return self.score

    def hide(self) -> None:
        self.get_item().hide()

    def show(self) -> None:
        self.get_item().show()