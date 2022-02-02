
from PyQt5.QtGui import QFont
from activities.activity import Activity
from ui.components.button_component import ButtonComponent
from ui.components.skeleton_component import SkeletonComponent
from ui.pygame.pygame_button import PyGameButton
from ui.pygame.pygame_skeleton import PyGameSkeleton
import pyqtgraph as pg
import random



class Game(Activity):

    def __init__(self, body_point_array, **kwargs) -> None:
        super().__init__(body_point_array, **kwargs)
        self.persist = {}
        self.persist["skeleton"] = PyGameSkeleton(body_point_array)
        #self.persist["timer"] = TimerUIComponent(0.4, -1.2, font=QFont("Arial", 30), text="Time: ", starting_time=0, func=self.time_expire_func)

        stage_0 = {}
        #stage_0["start_button"] = PyGameButton(50, (0, 255, 0, 120), 0, -0.6, func=self.start_button_func, target_pts=[16, 15])

        stage_1 = {}
        #stage_1["target_1"] = PyGameButton(50, (255, 0, 0, 120), random.uniform(-0.7, 0.7), random.uniform(0.0, -0.8), func=self.target_1_func, target_pts=[15])
        #stage_1["target_2"] = PyGameButton(50, (0, 0, 255, 120), random.uniform(-0.7, 0.7), random.uniform(0.0, -0.8), func=self.target_2_func, target_pts=[16])

        self.stages = [stage_0, stage_1]
        self.stage = 0

        self.components = self.stages[self.stage]

    def time_expire_func(self) -> None:
        self.stage = 0
        self.change_stage()
        if "stop_logging" in self.funcs:
            for func in self.funcs["stop_logging"]:
                func()
    
    def target_1_func(self) -> None:
        #self.stages[1]["target_1"].set_pos(random.uniform(-0.7,0.7), random.uniform(0.0,-0.8))
        pass

    def target_2_func(self) -> None:
        #self.stages[1]["target_2"].set_pos(random.uniform(-0.7,0.7), random.uniform(0.0,-0.8))
        pass

    def start_button_func(self) -> None:
        if self.stage == 0:
            #self.persist["timer"].set_timer(10)
            self.stage = self.stage + 1
            if "new_log" in self.funcs:
                for func in self.funcs["new_log"]:
                    func()
            if "start_logging" in self.funcs:
                for func in self.funcs["start_logging"]:
                    func()
            self.change_stage()
