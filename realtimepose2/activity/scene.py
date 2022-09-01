from typing import List
from realtimepose2.core.displaying.components import Component


class Scene:
    """"""


    def __init__(self) -> None:
        self.components: List[Component] = []

    def add_component(self, component: Component):
        self.components.append(component)