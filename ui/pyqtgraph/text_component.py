
from ui.pyqtgraph.component import Component
import pyqtgraph as pg

class TextComponent(Component):

    def __init__(self, x_pos: float, y_pos: float, **kwargs) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = "test"
        self.text_label = pg.TextItem(text=self.text)
        self.text_label.setPos(x_pos, y_pos)

        if "font" in kwargs:
            self.text_label.setFont(kwargs["font"])
        if "text" in kwargs:
            self.text_label.setText(kwargs["text"])

    def set_pos(self, x_pos: float, y_pos: float) -> None:
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_label.SetPos(x_pos, y_pos)

    def get_item(self) -> pg.TextItem:
        return self.text_label

    def set_text(self, text: str) -> None:
        self.text_label.setText(text)

    def get_text(self) -> str:
        return self.text
        