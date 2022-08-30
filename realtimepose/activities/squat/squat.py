
from PyQt5.QtGui import QFont
from activities.activity import Activity
from ui.components.component_factory import ComponentFactory
import pyqtgraph as pg
import random
from constants.constants import *


class Squat(Activity):

    def __init__(self, body_point_array, ui, **kwargs) -> None:
        super().__init__(body_point_array, ui, **kwargs)

        cf = ComponentFactory(self.ui)

        self.persist = {}

        self.persist[SKELETON] = cf.new_skeleton(body_point_array)
        self.persist[TIMER] = cf.new_timer(0.4, -1.2, font=QFont("Arial", 30), text="Time: ", starting_time=0, func=self.time_expire_func)

        stage_0 = {}
        stage_0[START_TARGET] = cf.new_button(50, pg.mkBrush(0, 255, 0, 120), 0, -0.6, func=self.start_button_func, target_pts=[16, 15])

        stage_1 = {}
        stage_1["target_1"] = cf.new_button(50, pg.mkBrush(255, 0, 0, 120), random.uniform(-0.7, 0.7), random.uniform(0.0, -0.8), func=self.target_1_func, target_pts=[15])
        stage_1["target_2"] = cf.new_button(50, pg.mkBrush(0, 0, 255, 120), random.uniform(-0.7, 0.7), random.uniform(0.0, -0.8), func=self.target_2_func, target_pts=[16])

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
            self.persist[TIMER].set_timer(10)
            self.stage = self.stage + 1
            self.change_stage()