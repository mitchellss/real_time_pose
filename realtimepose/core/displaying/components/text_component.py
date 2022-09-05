
class TextComponent:

    def __init__(self, x_pos: float, y_pos: float, text: str, **kwargs) -> None:
        super().__init__(x_pos, y_pos)
        self.text = text
        if "font" in kwargs:
            self.font = kwargs["font"]
        else:
            self.font = "Arial"
        
        if "size" in kwargs:
            self.size = kwargs["size"]
        else:
            self.size = 30

        if "color" in kwargs:
            self.color = kwargs["color"]
        else:
            self.color = (255, 255, 255)

    def set_text(self, text: str) -> None:
        self.text = text

    def get_text(self) -> None:
        return self.text