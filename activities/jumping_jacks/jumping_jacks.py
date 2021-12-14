
from PyQt5.QtGui import QFont
from activities.activity import Activity
from constants.constants import PATH
from ui.pyqtgraph.button_component import ButtonComponent
from ui.pyqtgraph.skeleton_component import SkeletonComponent
from ui.pyqtgraph.timer_component import TimerComponent
import pyqtgraph as pg

class JumpingJacks(Activity):

    def __init__(self, body_point_array, **kwargs) -> None:
        self.persist = {}
        self.persist["skeleton"] = SkeletonComponent(body_point_array)
        self.persist["timer"] = TimerComponent(0.4, -1.2, font=QFont("Arial", 30), text="Time: ", starting_time=0, func=self.time_expire_func)

        stage_0 = {}
        stage_0["start_button"] = ButtonComponent(50, pg.mkBrush(0, 255, 0, 120), 0, -0.6, func=self.start_button_func, target_pts=[16, 15])

        self.lh_points_file = open(PATH / "activities" / "jumping_jacks" / "lh_points.csv")
        self.rh_points_file = open(PATH / "activities" / "jumping_jacks" / "rh_points.csv")
        lh_line = self.lh_points_file.readline().split(",")
        rh_line = self.rh_points_file.readline().split(",")

        stage_1 = {}
        stage_1["target_1"] = ButtonComponent(50, pg.mkBrush(255, 0, 0, 120), float(lh_line[0]), float(lh_line[1]), func=self.target_1_func, target_pts=[15])
        stage_1["target_2"] = ButtonComponent(50, pg.mkBrush(0, 0, 255, 120), float(rh_line[0]), float(rh_line[1]), func=self.target_2_func, target_pts=[16])

        self.stages = [stage_0, stage_1]
        self.stage = 0

        self.components = self.stages[self.stage]

    def time_expire_func(self):
        self.stage = 0
        self.change_stage()
        self.lh_points_file.close()
        self.rh_points_file.close()
    
    def target_1_func(self):
        try:
            lh_line = self.lh_points_file.readline().split(",")
            self.stages[1]["target_1"].set_pos(float(lh_line[0]), float(lh_line[1]))
        except:
            True

    def target_2_func(self):
        try:
            rh_line = self.rh_points_file.readline().split(",")
            self.stages[1]["target_2"].set_pos(float(rh_line[0]), float(rh_line[1]))
        except:
            True

    def start_button_func(self):
        if self.stage == 0:
            self.lh_points_file = open(PATH / "activities" / "jumping_jacks" / "lh_points.csv")
            self.rh_points_file = open(PATH / "activities" / "jumping_jacks" / "rh_points.csv")
            lh_line = self.lh_points_file.readline().split(",")
            rh_line = self.rh_points_file.readline().split(",")
            self.stages[1]["target_1"].set_pos(float(lh_line[0]), float(lh_line[1]))
            self.stages[1]["target_2"].set_pos(float(rh_line[0]), float(rh_line[1]))

            self.persist["timer"].set_timer(10)
            self.stage = self.stage + 1
            self.change_stage()