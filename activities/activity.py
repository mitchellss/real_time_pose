
from typing import Dict
from ui.pyqtgraph.button_component import ButtonComponent
from ui.pyqtgraph.component import Component
from constants.constants import *

class Activity():

    def __init__(self, body_point_array, **kwargs) -> None:
        if "funcs" in kwargs:
            self.funcs = kwargs["funcs"]
        else:
            self.funcs = {}

    def get_stages(self) -> list[Dict[str, Component]]:
        return self.stages

    def get_persist(self) -> Dict[str, Component]:
        return self.persist

    def get_current_stage(self) -> int:
        return self.stage

    def set_current_stage(self, stage: int) -> None:
        self.stage = stage

    def get_components(self) -> Dict[str, Component]:
        return self.components

    def set_components(self, components: Dict[str, Component]) -> None:
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

    def handle_frame(self) -> None:
        """
        Defines the generic functionality of commonly used components. Override
        this method for complete custom functionality or call it and add to it in 
        the child class's method
        """
        for component in self.components: # For each component in the dict of active components
            # Handles the logic for buttons
            if isinstance(self.components[component], ButtonComponent):
                # Check to see if each of the target points on the skeleton are touching the button
                for target in self.components[component].target_pts:
                    x: float = self.persist[SKELETON].skeleton_array[target][0]
                    y: float = self.persist[SKELETON].skeleton_array[target][1]
                    
                    if self.components[component].is_clicked(x, y, self.components[component].precision):
                        break # Stops rest of for loop from running (caused errors)    
