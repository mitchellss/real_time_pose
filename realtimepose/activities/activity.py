
from typing import Dict

from realtimepose.pose_detection.pose_detection import PoseDetection

from ..data_logging.logger import Logger

from ..ui.components.button_component import ButtonComponent
from ..ui.components.hand_bubble_component import HandBubbleComponent
from ..ui.ui_component import UIComponent
from ..constants.constants import *
from typing_extensions import Protocol
from .scene import Scene


class Activity:
    """
    Represents an activity. An activity is a group of related scenes
    and the logic that controls both the switching between said
    scenes and the values/behaviour of the components that make up
    the scenes themselves.
    """

    active_components: Dict[str, UIComponent] = {}
    scenes: list[Scene] = []
    active_scene: int = 0

    def __init__(self, input: PoseDetection, frontend: GUI) -> None:
        self.input = input
        self.frontend = frontend

    # def __init__(self, body_point_array, ui, **kwargs) -> None:
    #     self.components: Dict[str, UIComponent] = None
    #     self.persist: Dict[str, UIComponent] = None
    #     self.scenes: list[Dict[str, UIComponent]] = None
    #     self.scene: int = 0
    #     self.ui = ui
    #     if FUNCS in kwargs:
    #         self.funcs = kwargs[FUNCS]
    #     else:
    #         self.funcs = {}

    #     # Initialize path variable if specified in kwargs
    #     if PATH_ARG in kwargs:
    #         self.file_path = kwargs[PATH_ARG]
    
    def add_scene(self, scene: Scene):
        """Appends a new scene to the activity"""
        self.scenes.append(scene)
    
    def add_logger(self, logger: Logger):
        pass

    def get_scenes(self) -> list[Dict[str, UIComponent]]:
        """
        Returns the list of scenes that make up the activity 
        in the order they were added
        """
        return self.scenes

    def get_persist(self) -> Dict[str, UIComponent]:
        return self.persist

    def get_current_scene(self) -> int:
        """Returns the currently active scene"""
        return self.scene

    def set_current_scene(self, scene: int) -> None:
        """Sets the current scene to the scene specified by the provided index"""
        self.scene = scene

    def next_scene(self) -> None:
        """TODO"""
    
    def previous_scene(self) -> None:
        """TODO"""

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

