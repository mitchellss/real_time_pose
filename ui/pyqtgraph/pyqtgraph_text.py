from ui.components.text_component import TextComponent
import pyqtgraph as pg
from PyQt5.QtGui import QFont

class PyQtGraphText(TextComponent):

    def __init__(self, x_pos: float, y_pos: float, text: str, **kwargs) -> None:
        super().__init__(x_pos, y_pos, text)
        self.text_label = pg.TextItem(text=self.text)
        self.text_label.setPos(x_pos, y_pos)
        self.text_label.setFont(QFont(self.font, self.size))

    def set_pos(self, x_pos: float, y_pos: float) -> None:
        super().set_pos(x_pos, y_pos)
        self.text_label.SetPos(x_pos, y_pos)

    def get_item(self) -> pg.TextItem:
        return self.text_label

    def set_text(self, text: str) -> None:
        self.text = text
        self.text_label.setText(self.text)

    def get_text(self) -> str:
        return self.text
        