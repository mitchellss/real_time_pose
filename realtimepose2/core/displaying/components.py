
from typing_extensions import Protocol

class Component(Protocol):
    x: float
    y: float

    def render(self):
        """"""

class Button(Protocol):
    x: float
    y: float
    def is_clicked(self, x: float, y: float, distance: float) -> bool:
        """"""

    def render(self):
        """"""
    
class HasButton(Protocol):
    def button(self, x: float, y: float) -> Button:
        """"""

def button(ui: HasButton, x: float, y: float) -> Button:
    return button_impl(ui, x, y)

class button_impl:
    def __init__(self, ui: HasButton, x: float, y: float) -> None:
        self.ui = ui
        self.x = x
        self.y = y
    
    def is_clicked(self, x: float, y: float, distance: float) -> bool:
        if abs(self.x - x) < distance and abs(self.y - y) < distance:
            return True
        return False
    
    def render(self):
        print("Shared render logic")
        self.ui.button(self.x, self.y).render()