
class Activity():

    def __init__(self, body_point_array) -> None:
        pass

    def get_stages(self) -> list:
        return self.stages

    def get_persist(self) -> dict:
        return self.persist

    def get_current_stage(self) -> int:
        return self.stage

    def set_current_stage(self, stage) -> None:
        self.stage = stage

    def get_components(self):
        return self.components

    def set_components(self, components):
        self.components = components

    def change_stage(self):
        # Hides old components
        for component in self.components:
            self.components[component].hide()

        # Switches out new components
        self.components = self.stages[self.stage]

        # Shows new components
        for component in self.components:
            self.components[component].show()