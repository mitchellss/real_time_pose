

from ui.ui_component import UIComponent


class TextComponent(UIComponent):

    def __init__(self, x_pos: float, y_pos: float, text: str) -> None:
        super().__init__(x_pos, y_pos)
        self.text = text

    def set_text(self, text: str) -> None:
        self.text = text

    def get_text(self) -> None:
        return self.text