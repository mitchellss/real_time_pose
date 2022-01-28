
from typing import Dict
from ui.pyqtgraph.component import Component


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

    def end_frame_reset(self) -> None:
        pass