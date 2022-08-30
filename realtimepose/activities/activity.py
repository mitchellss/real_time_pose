
from typing import Dict

from ui.components.button_component import ButtonComponent
from ui.components.hand_bubble_component import HandBubbleComponent
from ui.ui_component import UIComponent
from constants.constants import *
from typing_extensions import Protocol


class Activity(Protocol):

    def __init__(self, body_point_array, ui, **kwargs) -> None:
        self.components: Dict[str, UIComponent] = None
        self.persist: Dict[str, UIComponent] = None
        self.scenes: list[Dict[str, UIComponent]] = None
        self.scene: int = 0
        self.ui = ui
        if FUNCS in kwargs:
            self.funcs = kwargs[FUNCS]
        else:
            self.funcs = {}

        # Initialize path variable if specified in kwargs
        if PATH_ARG in kwargs:
            self.file_path = kwargs[PATH_ARG]
    
    def add_scene(self, scene: Scene):
        self.scenes.append(scene)

    def get_scenes(self) -> list[Dict[str, UIComponent]]:
        return self.scenes

    def get_persist(self) -> Dict[str, UIComponent]:
        return self.persist

    def get_current_scene(self) -> int:
        return self.scene

    def set_current_scene(self, scene: int) -> None:
        self.scene = scene

    def get_components(self) -> Dict[str, UIComponent]:
        return self.components

    def set_components(self, components: Dict[str, UIComponent]) -> None:
        self.components = components

    def change_scene(self) -> None:
        # Hides old components
        for component in self.components:
            self.components[component].hide()

        # Switches out new components
        self.components = self.scenes[self.scene]

        # Shows new components
        for component in self.components:
            self.components[component].show()
    
    def run(self) -> None:
        while True:
            self.body_point_array = self.skeleton.get_points()
            self.loggers.log_data()
            self.handle_frame()
            self.gui.update()

    def handle_frame(self, **kwargs) -> None:
        """
        Defines the generic functionality of commonly used components. Override
        this method for complete custom functionality or call it and add to it in 
        the child class's method
        """
        for component in self.components:
            if "surface" in kwargs:
                self.components[component].draw(kwargs["surface"])

        for component in self.persist:
            if "surface" in kwargs:
                self.persist[component].draw(kwargs["surface"])

        for component in self.components: # For each component in the dict of active components
            # Handles the logic for buttons
            if isinstance(self.components[component], ButtonComponent):
                # Check to see if each of the target points on the skeleton are touching the button
                for target in self.components[component].target_pts:
                    x: float = self.persist[SKELETON].skeleton_array[target][0]
                    y: float = self.persist[SKELETON].skeleton_array[target][1]
                    
                    if self.components[component].is_clicked(x, y, self.components[component].precision):
                        break # Stops rest of for loop from running (caused errors) 

            if isinstance(self.components[component], HandBubbleComponent):
                target = self.components[component].target
                x: float = self.persist[SKELETON].skeleton_array[target][0]
                y: float = self.persist[SKELETON].skeleton_array[target][1]
                self.components[component].set_pos(x, y)

