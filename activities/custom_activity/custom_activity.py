from pyqtgraph.functions import mkBrush
from activities.activity import Activity
from ui.pyqtgraph.button_component import ButtonComponent
from ui.pyqtgraph.skeleton_component import SkeletonComponent
from ui.pyqtgraph.timer_component import TimerComponent
from PyQt5.QtGui import QFont
from constants.constants import PATH
import sys
import pandas as pd

class CustomActivity(Activity):
    """Activity that takes a custom file as the input and replays it for the user to replicate.

    Args:
        Activity ([type]): Abstract activity object
    """

    def __init__(self, body_point_array, **kwargs) -> None:

        # Initialize persistant component dict (Never dissapear reguardless of active stage)
        self.persist = {}
        self.persist["skeleton"] = SkeletonComponent(body_point_array)
        self.persist["timer"] = TimerComponent(0.4, -1.2, font=QFont("Arial", 30), text="Time: ", starting_time=0, func=self.time_expire_func)

        # Initialize dict for stage 0 
        stage_0 = {}
        stage_0["start_button"] = ButtonComponent(50, mkBrush(0, 255, 0, 120), 0, -0.6, func=self.start_button_func, target_pts=[16, 15])

        # Initialize path variable if specified in kwargs
        if "path" in kwargs:
            self.file_path = kwargs["path"]

        # Attempts to read point data from specified CSV, otherwise exits
        try:
            points_data = pd.read_csv(self.file_path)
        except:
            print("Cannot find csv file specified")
            sys.exit(1)

        # Set data for each point (based on https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png)
        self.lh_x_data = points_data["x15"]
        self.lh_y_data = points_data["y15"]

        self.rh_x_data = points_data["x16"]
        self.rh_y_data = points_data["y16"]

        self.ll_x_data = points_data["x27"]
        self.ll_y_data = points_data["y27"]

        self.rl_x_data = points_data["x28"]
        self.rl_y_data = points_data["y28"]
        
        # Index tracks point in the file for a specific group of buttons/points
        self.index = 0

        # Initialize stage 1 dict. This contains all the buttons
        stage_1 = {}
        stage_1["target_1"] = ButtonComponent(50, mkBrush(255, 0, 0, 120), 
            float(self.lh_x_data[self.index]), float(self.lh_y_data[self.index]), 
            func=self.target_1_func, target_pts=[15], precision=0.3)

        stage_1["target_2"] = ButtonComponent(50, mkBrush(0, 0, 255, 120), 
            float(self.rh_x_data[self.index]), float(self.rh_y_data[self.index]), 
            func=self.target_2_func, target_pts=[16], precision=0.3)

        stage_1["target_3"] = ButtonComponent(50, mkBrush(100, 100, 0, 120), 
            float(self.ll_x_data[self.index]), float(self.ll_y_data[self.index]), 
            func=self.target_3_func, target_pts=[27], precision=0.3)

        stage_1["target_4"] = ButtonComponent(50, mkBrush(0, 100, 100, 120), 
            float(self.rl_x_data[self.index]), float(self.rl_y_data[self.index]), 
            func=self.target_4_func, target_pts=[28], precision=0.3)

        # Initializes a dict of functions where various capabilities can be passed
        # i.e (Start logging, stop logging, etc.)
        if "funcs" in kwargs:
            self.funcs = kwargs["funcs"]
        else:
            self.funcs = {}

        # List of stages to swap between and what stage to start at
        self.stages = [stage_0, stage_1]
        self.stage = 0

        # # Use this to start at stage 1
        # self.stage = 1
        # self.persist["timer"].set_timer(100)

        # Set the active components to the dict of the initial stage
        self.components = self.stages[self.stage]

    def time_expire_func(self) -> None:
        if self.stage != 0:
            self.stage = 0
            self.index = 0
            self.change_stage()
            if "stop_logging" in self.funcs:
                for func in self.funcs["stop_logging"]:
                    func()
    
    def target_1_func(self) -> None:
        self.stages[1]["target_1"].clicked = True
        if self.stages[1]["target_2"].clicked and self.stages[1]["target_3"].clicked and self.stages[1]["target_4"].clicked:
            self.index += 1
            self.stages[1]["target_1"].set_pos(float(self.lh_x_data[self.index]), float(self.lh_y_data[self.index]))
            self.stages[1]["target_2"].set_pos(float(self.rh_x_data[self.index]), float(self.rh_y_data[self.index]))
            self.stages[1]["target_3"].set_pos(float(self.ll_x_data[self.index]), float(self.ll_y_data[self.index]))
            self.stages[1]["target_4"].set_pos(float(self.rl_x_data[self.index]), float(self.rl_y_data[self.index]))

    def target_2_func(self) -> None:
        self.stages[1]["target_2"].clicked = True
        if self.stages[1]["target_1"].clicked and self.stages[1]["target_3"].clicked and self.stages[1]["target_4"].clicked:
            self.index += 1
            self.stages[1]["target_1"].set_pos(float(self.lh_x_data[self.index]), float(self.lh_y_data[self.index]))
            self.stages[1]["target_2"].set_pos(float(self.rh_x_data[self.index]), float(self.rh_y_data[self.index]))
            self.stages[1]["target_3"].set_pos(float(self.ll_x_data[self.index]), float(self.ll_y_data[self.index]))
            self.stages[1]["target_4"].set_pos(float(self.rl_x_data[self.index]), float(self.rl_y_data[self.index]))

    def target_3_func(self) -> None:
        self.stages[1]["target_3"].clicked = True
        if self.stages[1]["target_1"].clicked and self.stages[1]["target_2"].clicked and self.stages[1]["target_4"].clicked:
            self.index += 1
            self.stages[1]["target_1"].set_pos(float(self.lh_x_data[self.index]), float(self.lh_y_data[self.index]))
            self.stages[1]["target_2"].set_pos(float(self.rh_x_data[self.index]), float(self.rh_y_data[self.index]))
            self.stages[1]["target_3"].set_pos(float(self.ll_x_data[self.index]), float(self.ll_y_data[self.index]))
            self.stages[1]["target_4"].set_pos(float(self.rl_x_data[self.index]), float(self.rl_y_data[self.index]))

    def target_4_func(self) -> None:
        self.stages[1]["target_4"].clicked = True
        if self.stages[1]["target_1"].clicked and self.stages[1]["target_2"].clicked and self.stages[1]["target_3"].clicked:
            self.index += 1
            self.stages[1]["target_1"].set_pos(float(self.lh_x_data[self.index]), float(self.lh_y_data[self.index]))
            self.stages[1]["target_2"].set_pos(float(self.rh_x_data[self.index]), float(self.rh_y_data[self.index]))
            self.stages[1]["target_3"].set_pos(float(self.ll_x_data[self.index]), float(self.ll_y_data[self.index]))
            self.stages[1]["target_4"].set_pos(float(self.rl_x_data[self.index]), float(self.rl_y_data[self.index]))

    def start_button_func(self) -> None:
        """
        Defines what should happen when the start button is pressed. In this
        case, it sets the timer to 100, increments the stage, creates new logs,
        starts the logs, and activates the stage change.
        """
        if self.stage == 0:
            self.persist["timer"].set_timer(100)
            self.stage = self.stage + 1
            if "new_log" in self.funcs:
                for func in self.funcs["new_log"]:
                    func()
            if "start_logging" in self.funcs:
                for func in self.funcs["start_logging"]:
                    func()
            self.change_stage()

    def handle_frame(self) -> None:
        """
        Defines what should happen at the end of a frame. In this case, it
        resets all the buttons to no longer be clicked.
        """
        self.stages[1]["target_1"].clicked = False
        self.stages[1]["target_2"].clicked = False
        self.stages[1]["target_3"].clicked = False
        self.stages[1]["target_4"].clicked = False
