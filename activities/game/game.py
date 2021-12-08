
from PyQt5.QtGui import QFont
from activities.activity import Activity
from ui.pyqtgraph.button_component import ButtonComponent
from ui.pyqtgraph.skeleton_component import SkeletonComponent
from ui.pyqtgraph.timer_component import TimerComponent
import pyqtgraph as pg
import random


class Game(Activity):

    def __init__(self, body_point_array, change_stage_func) -> None:

        # Coordinates for the targets for the user to pop
        self.target_1_x = random.uniform(-0.7,0.7)
        self.target_1_y = random.uniform(0.0,-0.8)
        self.target_2_x = random.uniform(-0.7,0.7)
        self.target_2_y = random.uniform(0.0,-0.8)

        # Coordinates for start target
        self.start_target_x = 0
        self.start_target_y = -0.6

        self.change_stage_func = change_stage_func

        self.persist = {}
        self.persist["skeleton"] = SkeletonComponent(body_point_array)
        self.persist["timer"] = TimerComponent(0.4, -1.2, font=QFont("Arial", 30), text="Time: ", starting_time=0, func=self.time_expire_func)

        stage_0 = {}
        stage_0["start_button"] = ButtonComponent(50, pg.mkBrush(0, 255, 0, 120), self.start_target_x, self.start_target_y, func=self.start_button_func, target_pts=[16, 15])

        stage_1 = {}
        stage_1["target_1"] = ButtonComponent(50, pg.mkBrush(255, 0, 0, 120), self.target_1_x, self.target_1_y, func=self.target_1_func, target_pts=[15])
        stage_1["target_2"] = ButtonComponent(50, pg.mkBrush(0, 0, 255, 120), self.target_2_x, self.target_2_y, func=self.target_2_func, target_pts=[16])

        self.stages = [stage_0, stage_1]
        self.stage = 0

    def get_stages(self) -> list:
        return self.stages

    def get_persist(self) -> dict:
        return self.persist

    def get_current_stage(self) -> int:
        return self.stage

    def set_current_stage(self, stage) -> None:
        self.stage = stage

    def time_expire_func(self):
        self.stage = 0
        self.change_stage_func()
    
    def target_1_func(self):
        self.stages[1]["target_1"].set_pos(random.uniform(-0.7,0.7), random.uniform(0.0,-0.8))

    def target_2_func(self):
        self.stages[1]["target_2"].set_pos(random.uniform(-0.7,0.7), random.uniform(0.0,-0.8))

    def start_button_func(self):
        self.persist["timer"].set_timer(10)
        self.stage = self.stage + 1
        self.change_stage_func()