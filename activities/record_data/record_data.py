from activities.activity import Activity
from ui.components.component_factory import ComponentFactory
from constants.constants import *
import sys
import pandas as pd
from better_profanity import profanity

from utils.utils import *


class RecordData(Activity):
    """Second version of the original game. Buttons move around and players have
    to keep their hands in them as long as possible to earn the highest score.

    Args:
        Activity ([type]): Abstract activity object
    """

    STARTING_STAGE = 0
    PLAY_STAGE = 1

    def __init__(self, body_point_array, ui, **kwargs) -> None:
        super().__init__(body_point_array, ui, **kwargs)

        cf = ComponentFactory(self.ui)

        # Initialize persistant component dict (Never dissapear reguardless of active stage)
        self.persist = {}
        self.persist[SKELETON] = cf.new_skeleton(body_point_array)
        self.persist[TIMER] = cf.new_timer(WINDOW_WIDTH-250, 60, size=50, func=lambda: True)
        self.persist[TIMER].hide()

        # Initialize dict for stage 0 
        stage_0 = {}
        stage_0[START_TARGET] = cf.new_button(50, (255, 0, 0, 120),
                                                     WINDOW_WIDTH-250, WINDOW_HEIGHT/2-100, func=self.start_button_func, target_pts=[16], precision=50)
        stage_0["bubble_0"] = cf.new_hand_bubble(0, 0, 16, 30, (255, 0, 0, 120))

        stage_1 = {}
        stage_1["bubble_1"] = cf.new_hand_bubble(0, 0, 15, 30, (0, 0, 255, 120))
        stage_1["submit_button"] = cf.new_button(50, (0, 0, 255, 120),
                                                     WINDOW_WIDTH-750, WINDOW_HEIGHT/2-100, func=self.submit_score_func, target_pts=[15], precision=50)


        # List of stages to swap between and what stage to start at
        self.stages = [stage_0, stage_1]
        self.stage = 0


        # Set the active components to the dict of the initial stage
        self.components = self.stages[self.stage]



    def submit_score_func(self):
        self.stage = 0
        if STOP_LOGGING in self.funcs:
            for func in self.funcs[STOP_LOGGING]:
                func()


    def start_button_func(self) -> None:
        """
        Defines what should happen when the start button is pressed. In this
        case, it sets the timer to 100, increments the stage, creates new logs,
        starts the logs, and activates the stage change.
        """
        if self.stage == 0:
            self.stage = self.stage + 1
            if NEW_LOG in self.funcs:
                for func in self.funcs[NEW_LOG]:
                    func()
            if START_LOGGING in self.funcs:
                for func in self.funcs[START_LOGGING]:
                    func()

    def handle_frame(self, **kwargs) -> None:
        """
        Defines what should happen at the end of a frame. In this case, it
        resets all the buttons to no longer be clicked.
        """
        super().handle_frame(**kwargs)


        self.change_stage()
