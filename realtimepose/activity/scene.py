"""Class and logic that create an abstract scene."""
from typing import List
from realtimepose.core.displaying.components import Component


class Scene:
    """A related group of components that should
    be rendered at the same time."""

    def __init__(self) -> None:
        """Creates a new scene.
        """
        self.components: List[Component] = []

    def add_component(self, component: Component) -> None:
        """Adds a component to the list of components for
        the scene.

        Args:
            component (Component): The component to add.
        """
        self.components.append(component)
