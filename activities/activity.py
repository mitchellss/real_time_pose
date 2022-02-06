
from typing import Dict

from ui.components.button_component import ButtonComponent
from ui.components.hand_bubble_component import HandBubbleComponent
from ui.ui_component import UIComponent
from constants.constants import *


class Activity:

    def __init__(self, body_point_array, **kwargs) -> None:
        self.components: Dict[str, UIComponent] = None
        self.persist: Dict[str, UIComponent] = None
        self.stages: list[Dict[str, UIComponent]] = None
        self.stage: int = 0
        if FUNCS in kwargs:
            self.funcs = kwargs[FUNCS]
        else:
            self.funcs = {}

    def get_stages(self) -> list[Dict[str, UIComponent]]:
        return self.stages

    def get_persist(self) -> Dict[str, UIComponent]:
        return self.persist

    def get_current_stage(self) -> int:
        return self.stage

    def set_current_stage(self, stage: int) -> None:
        self.stage = stage

    def get_components(self) -> Dict[str, UIComponent]:
        return self.components

    def set_components(self, components: Dict[str, UIComponent]) -> None:
        self.components = components

    def change_stage(self) -> None:
        # Hides old components
        for component in self.components:
            self.components[component].hide()

        # Switches out new components
        self.components = self.stages[self.stage]

        # Shows new components
        for component in self.components:
            self.components[component].show()

    def handle_frame(self, **kwargs) -> None:
        """
        Defines the generic functionality of commonly used components. Override
        this method for complete custom functionality or call it and add to it in 
        the child class's method
        """
        for component in self.components:
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

