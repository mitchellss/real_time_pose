from realtimepose2.core.displaying.components import Button

class Pyglet:
    """"""
    def add_component(self, component):
        """"""
    
    def clear(self):
        """"""
    
    def button(self, x:float, y:float) -> Button:
        return PygletButton(x, y)
    
class PygletButton:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def is_clicked(self, x: float, y:float, distance: float) -> bool:
        return False
    
    def render(self):
        print("pyglet render")