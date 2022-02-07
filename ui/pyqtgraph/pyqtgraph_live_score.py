import pyqtgraph as pg
from ui.components.live_score_component import LiveScoreComponent
from PyQt5.QtGui import QFont


class PyQtGraphLiveScore(LiveScoreComponent):
    """Component used to create a text score counter that can
    be updated in real-time

    Args:
        Component (): Abstract component type
    """
    def __init__(self, x_pos: float, y_pos: float, **kwargs) -> None:
        super().__init__(x_pos, y_pos, **kwargs)
        self.score_count = pg.TextItem(text="Score: ")
        self.score_count.setPos(self.x_pos, self.y_pos)
        self.score_count.setFont(QFont(self.font, self.size))
        self.score_count.setText(self.text)
    
    def set_pos(self, x_pos: float, y_pos: float):
        super().set_pos(x_pos, y_pos)
        self.score_count.SetPos(x_pos, y_pos)

    def get_item(self) -> pg.TextItem:
        return self.score_count

    def set_score(self, score: int) -> None:
        super().set_score(score)
        self.score_count.setText(f"Score: {self.score}")

    def add_score(self, score: int) -> None:
        super().add_score(score)
        self.score_count.setText(f"Score: {self.score}")

    def hide(self) -> None:
        self.get_item().hide()

    def show(self) -> None:
        self.get_item().show()