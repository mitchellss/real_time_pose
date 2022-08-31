
from ..ui_component import UIComponent


class LiveScoreComponent(UIComponent):
    
    def __init__(self, x_pos: float, y_pos: float, **kwargs) -> None:
        super().__init__(x_pos, y_pos)
        self.score: int = 0

        if "font" in kwargs:
            self.font = kwargs["font"]
        else:
            self.font = "Arial"

        if "size" in kwargs:
            self.size = kwargs["size"]
        else:
            self.size = 30

        if "text" in kwargs:
            self.text = kwargs["text"]
        else:
            self.text = f"Score: {self.score}"
    
    def set_score(self, score: int) -> None:
        self.score = score

    def add_score(self, score: int) -> None:
        self.score += score

    def get_score(self) -> int:
        return self.score


