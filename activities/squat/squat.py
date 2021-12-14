
from PyQt5.QtGui import QFont
from activities.activity import Activity
from ui.pyqtgraph.button_component import ButtonComponent
from ui.pyqtgraph.skeleton_component import SkeletonComponent
from ui.pyqtgraph.timer_component import TimerComponent
import pyqtgraph as pg
import random


class Squat(Activity):

    def __init__(self, body_point_array, **kwargs) -> None:
        self.persist = {}
        self.persist["skeleton"] = SkeletonComponent(body_point_array)
        self.persist["timer"] = TimerComponent(0.4, -1.2, font=QFont("Arial", 30), text="Time: ", starting_time=0, func=self.time_expire_func)

        stage_0 = {}
        stage_0["start_button"] = ButtonComponent(50, pg.mkBrush(0, 255, 0, 120), 0, -0.6, func=self.start_button_func, target_pts=[16, 15])

        stage_1 = {}
        stage_1["target_1"] = ButtonComponent(50, pg.mkBrush(255, 0, 0, 120), random.uniform(-0.7,0.7), random.uniform(0.0,-0.8), func=self.target_1_func, target_pts=[15])
        stage_1["target_2"] = ButtonComponent(50, pg.mkBrush(0, 0, 255, 120), random.uniform(-0.7,0.7), random.uniform(0.0,-0.8), func=self.target_2_func, target_pts=[16])

        self.stages = [stage_0, stage_1]
        self.stage = 0

        self.components = self.stages[0]

    def time_expire_func(self):
        self.stage = 0
        self.change_stage()
    
    def target_1_func(self):
        self.stages[1]["target_1"].set_pos(random.uniform(-0.7,0.7), random.uniform(0.0,-0.8))

    def target_2_func(self):
        self.stages[1]["target_2"].set_pos(random.uniform(-0.7,0.7), random.uniform(0.0,-0.8))

    def start_button_func(self):
        if self.stage == 0:
            self.persist["timer"].set_timer(10)
            self.stage = self.stage + 1
            self.change_stage()