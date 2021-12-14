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

    def __init__(self, body_point_array, **kwargs) -> None:
        self.persist = {}
        self.persist["skeleton"] = SkeletonComponent(body_point_array)
        self.persist["timer"] = TimerComponent(0.4, -1.2, font=QFont("Arial", 30), text="Time: ", starting_time=0, func=self.time_expire_func)

        stage_0 = {}
        stage_0["start_button"] = ButtonComponent(50, mkBrush(0, 255, 0, 120), 0, -0.6, func=self.start_button_func, target_pts=[16, 15])

        if "path" in kwargs:
            self.file_path = kwargs["path"]

        try:
            points_data = pd.read_csv(self.file_path)
        except:
            print("Cannot find csv file specified")
            sys.exit(1)

        self.lh_x_data = points_data["x15"]
        self.lh_y_data = points_data["y15"]
        self.lh_index = 0

        self.rh_x_data = points_data["x16"]
        self.rh_y_data = points_data["y16"]
        self.rh_index = 0

        stage_1 = {}
        stage_1["target_1"] = ButtonComponent(50, mkBrush(255, 0, 0, 120), float(self.lh_x_data[self.lh_index]), float(self.lh_y_data[self.lh_index]), func=self.target_1_func, target_pts=[15])
        stage_1["target_2"] = ButtonComponent(50, mkBrush(0, 0, 255, 120), float(self.rh_x_data[self.rh_index]), float(self.rh_y_data[self.rh_index]), func=self.target_2_func, target_pts=[16])

        if "funcs" in kwargs:
            self.funcs = kwargs["funcs"]
        else:
            self.funcs = {}


        self.stages = [stage_0, stage_1]
        self.stage = 0

        self.components = self.stages[self.stage]

    def time_expire_func(self) -> None:
        self.stage = 0
        self.lh_index = 0
        self.rh_index = 0
        self.change_stage()
        if "stop_logging" in self.funcs:
            for func in self.funcs["stop_logging"]:
                func()
    
    def target_1_func(self) -> None:
        self.lh_index += 5
        self.stages[1]["target_1"].set_pos(float(self.lh_x_data[self.lh_index]), float(self.lh_y_data[self.lh_index]))

    def target_2_func(self) -> None:
        self.rh_index += 5
        self.stages[1]["target_2"].set_pos(float(self.rh_x_data[self.rh_index]), float(self.rh_y_data[self.rh_index]))

    def start_button_func(self) -> None:
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
